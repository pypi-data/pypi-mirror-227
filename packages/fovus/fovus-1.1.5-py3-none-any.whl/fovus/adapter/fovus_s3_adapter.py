import concurrent.futures
import json
import os
import time
from http import HTTPStatus
from typing import Any, Callable, TypedDict

import boto3
import botocore
from mypy_boto3_s3.client import S3Client
from mypy_boto3_s3.type_defs import ObjectTypeDef
from tqdm import tqdm

from fovus.constants.cli_constants import (
    CLI_ARGUMENTS,
    EXCLUDE_INPUT,
    EXCLUDE_OUTPUT,
    INCLUDE_INPUT,
    INCLUDE_OUTPUT,
    JOB_ID,
    SKIP_CREATE_JOB_INFO_FOLDER,
)
from fovus.exception.system_exception import SystemException
from fovus.exception.user_exception import UserException
from fovus.util.aws_util import AwsUtil
from fovus.util.file_util import FOVUS_JOB_INFO_FOLDER, FileUtil
from fovus.util.fovus_api_util import FovusApiUtil
from fovus.util.fovus_s3_adapter_util import FovusS3AdapterUtil
from fovus.util.util import Util

DOWNLOAD = "Download"
LOCAL_FILEPATH = "local_filepath"
SUCCESS = "success"
UPLOAD = "Upload"

JOB_DATA_FILENAME = "job_data.json"

SECONDS_PER_MINUTE = 60
S3_TIMEOUT_MINUTES = 60


class S3Info(TypedDict):
    s3_client: S3Client
    s3_bucket: str
    s3_prefix: str
    expires_at: float


# pylint: disable=R0902
class FovusS3Adapter:
    download_s3_info: S3Info
    upload_s3_info: S3Info

    def __init__(self, fovus_api_adapter, cli_dict, root_directory_path):
        self.fovus_api_adapter = fovus_api_adapter
        self.cli_dict = cli_dict
        self.local_root_directory_path = root_directory_path
        self.job_id = FovusApiUtil.get_job_id(self.cli_dict)

        # Assigned if upload function is called.
        self.local_filepath_list = None
        self.task_count = None
        self.total_file_size_bytes = None
        self.progress_bar = None
        self.download_s3_info = None
        self.upload_s3_info = None

    def get_job_id(self):
        return self.job_id

    def upload_files(self):
        self._instantiate_upload_instance_variables()
        self._validate_root_directory()
        FovusS3AdapterUtil.print_pre_operation_information(
            UPLOAD, len(self.local_filepath_list), self.total_file_size_bytes, self.task_count
        )
        self._operate_on_s3_in_parallel(self.local_filepath_list, self._upload_file)
        self._create_job_data_file()
        FovusS3AdapterUtil.print_post_operation_success(UPLOAD, is_success=True)

    def _validate_root_directory(self):
        if FileUtil.directory_contains_directory(self.local_root_directory_path, FOVUS_JOB_INFO_FOLDER):
            raise UserException(
                HTTPStatus.BAD_REQUEST,
                self.__class__.__name__,
                "Root directory cannot contain a .fovus folder. Please remove it and try again. "
                + "\nNote: The .fovus folder is hidden, so you may need to adjust your file explorer's settings "
                + "to show hidden folders.",
            )

    def _create_job_data_file(self):
        if self.cli_dict.get(SKIP_CREATE_JOB_INFO_FOLDER):
            print(
                f"The {SKIP_CREATE_JOB_INFO_FOLDER} flag is set, so the {FOVUS_JOB_INFO_FOLDER} folder will not be "
                "created. Future operations on this job will require manual job ID specification using one of the "
                f"following CLI arguments: {CLI_ARGUMENTS[JOB_ID]}."
            )
            return

        job_data = {
            "job_id": self.job_id,
        }
        fovus_job_info_directory_path = os.path.join(self.local_root_directory_path, FOVUS_JOB_INFO_FOLDER)
        os.makedirs(fovus_job_info_directory_path)
        job_data_filepath = os.path.join(fovus_job_info_directory_path, JOB_DATA_FILENAME)
        with FileUtil.open(job_data_filepath, "w") as job_data_file:
            json.dump(job_data, job_data_file)

    def download_files(self):
        s3_object_list = self._get_s3_object_list()
        s3_info = self._get_download_s3_info()
        s3_prefix = s3_info["s3_prefix"]
        objects_to_download, self.total_file_size_bytes, self.task_count = AwsUtil.get_s3_object_list_info(
            s3_object_list, s3_prefix, self.cli_dict[INCLUDE_OUTPUT], self.cli_dict[EXCLUDE_OUTPUT]
        )
        FovusS3AdapterUtil.print_pre_operation_information(
            DOWNLOAD, len(objects_to_download), self.total_file_size_bytes, self.task_count
        )
        FileUtil.create_missing_directories(
            self.local_root_directory_path,
            AwsUtil.get_all_directories(
                objects_to_download,
                s3_prefix,
                self.cli_dict[INCLUDE_OUTPUT],
                self.cli_dict[EXCLUDE_OUTPUT],
            ),
        )
        self._operate_on_s3_in_parallel(objects_to_download, self._download_file)
        FovusS3AdapterUtil.print_post_operation_success(DOWNLOAD, is_success=True)

    def _operate_on_s3_in_parallel(self, remaining_items, file_operation: Callable[[Any], Any]):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            self.progress_bar = tqdm(
                total=self.total_file_size_bytes,
                unit="B",
                desc="Progress",
                unit_scale=True,
                unit_divisor=1024,
            )
            while True:
                futures: list = []
                remaining_items = self._try_operate_on_file_list(file_operation, futures, executor, remaining_items)
                if not remaining_items:
                    self.progress_bar.close()
                    return

    def _try_operate_on_file_list(  # pylint: disable=too-many-arguments
        self,
        file_operation: Callable[[Any], Any],
        futures,
        executor,
        remaining_objects,
    ):
        failed_objects = []
        for obj in remaining_objects:
            futures.append(executor.submit(file_operation, obj))
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if not result[SUCCESS]:
                failed_objects.append(result[LOCAL_FILEPATH])
        return failed_objects

    def _instantiate_upload_instance_variables(self):
        print("Preparing to upload files.")
        self.local_filepath_list, self.task_count, self.total_file_size_bytes = FileUtil.get_files_in_directory(
            self.local_root_directory_path, self.cli_dict[INCLUDE_INPUT], self.cli_dict[EXCLUDE_INPUT]
        )
        self._validate_upload_job()

    def _validate_upload_job(self):
        errors = []
        if self.task_count == 0:
            errors.append("tasks")
        if len(self.local_filepath_list) == 0:
            errors.append("files")
        if errors:
            raise UserException(
                HTTPStatus.BAD_REQUEST,
                self.__class__.__name__,
                f"No {' or '.join(errors)} found to upload. Please check your include/exclude filters.",
            )

    def _upload_file(self, local_filepath: str):
        local_relative_filepath = os.path.relpath(local_filepath, self.local_root_directory_path)
        s3_info = self._get_upload_s3_info()
        s3_path = os.path.join(s3_info["s3_prefix"], local_relative_filepath)
        if Util.is_windows():
            s3_path = FileUtil.windows_to_unix_path(s3_path)

        result = {SUCCESS: True, LOCAL_FILEPATH: local_filepath}
        try:
            s3_info = self._get_upload_s3_info()
            s3_info["s3_client"].upload_file(
                local_filepath, s3_info["s3_bucket"], s3_path, Callback=self.progress_bar.update
            )
        except boto3.exceptions.S3UploadFailedError as error:
            if AwsUtil.is_expired_token_error(error):
                result[SUCCESS] = False
            else:
                raise SystemException(HTTPStatus.INTERNAL_SERVER_ERROR, error)  # pylint: disable=raise-missing-from
        return result

    def _get_s3_object_list(self) -> list[ObjectTypeDef]:
        s3_info = self._get_download_s3_info()
        response = s3_info["s3_client"].list_objects_v2(Bucket=s3_info["s3_bucket"], Prefix=s3_info["s3_prefix"])
        s3_objects_list: list[ObjectTypeDef] = response["Contents"]

        while "NextContinuationToken" in response:
            response = s3_info["s3_client"].list_objects_v2(
                Bucket=s3_info["s3_bucket"],
                Prefix=s3_info["s3_prefix"],
                ContinuationToken=response["NextContinuationToken"],
            )
            s3_objects_list.extend(response["Contents"])

        return s3_objects_list

    def _get_download_s3_info(self) -> S3Info:
        if self.download_s3_info and self.download_s3_info["expires_at"] > time.time():
            return self.download_s3_info

        expires_at = time.time() + SECONDS_PER_MINUTE * S3_TIMEOUT_MINUTES
        s3_client, s3_bucket, s3_prefix = self.fovus_api_adapter.get_temporary_s3_download_credentials(self.cli_dict)
        s3_prefix += self.job_id

        self.download_s3_info = {
            "s3_client": s3_client,
            "s3_bucket": s3_bucket,
            "s3_prefix": s3_prefix,
            "expires_at": expires_at,
        }
        return self.download_s3_info

    def _get_upload_s3_info(self) -> S3Info:
        if self.upload_s3_info and self.upload_s3_info["expires_at"] > time.time():
            return self.upload_s3_info

        expires_at = time.time() + SECONDS_PER_MINUTE * S3_TIMEOUT_MINUTES
        s3_client, s3_bucket, s3_prefix = self.fovus_api_adapter.get_temporary_s3_upload_credentials(self.cli_dict)
        s3_prefix += self.job_id

        self.upload_s3_info = {
            "s3_client": s3_client,
            "s3_bucket": s3_bucket,
            "s3_prefix": s3_prefix,
            "expires_at": expires_at,
        }
        return self.upload_s3_info

    def _download_file(self, s3_object):
        result = {SUCCESS: True}
        if not AwsUtil.s3_object_is_directory(s3_object):
            s3_info = self._get_download_s3_info()
            local_filepath = self._get_local_filepath(s3_object, s3_info["s3_prefix"])
            result[LOCAL_FILEPATH] = local_filepath

            if FileUtil.include_exclude_allows_path(
                os.path.relpath(local_filepath, self.local_root_directory_path),
                self.cli_dict[INCLUDE_OUTPUT],
                self.cli_dict[EXCLUDE_OUTPUT],
            ) and FovusS3AdapterUtil.should_download_file(local_filepath, s3_object):
                os.makedirs(os.path.dirname(local_filepath), exist_ok=True)
                try:
                    s3_info = self._get_download_s3_info()
                    s3_info["s3_client"].download_file(
                        s3_info["s3_bucket"], s3_object["Key"], local_filepath, Callback=self.progress_bar.update
                    )
                except botocore.exceptions.ClientError as error:
                    if AwsUtil.is_expired_token_error(error):
                        result[SUCCESS] = False
                    else:
                        raise SystemException(  # pylint: disable=raise-missing-from
                            HTTPStatus.INTERNAL_SERVER_ERROR, error
                        )
            else:
                self.progress_bar.update(s3_object["Size"])
        return result

    def _get_local_filepath(self, s3_object, s3_prefix):
        return os.path.join(
            self.local_root_directory_path, AwsUtil.get_s3_object_key_without_prefix(s3_object, s3_prefix)
        )
