from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional, Union

import pytz
from dateutil import parser
from pydantic import ConfigDict, field_validator

from fa_common import CamelModel
from fa_common.storage import File

# from fa_common.db import DocumentDBModel


class ModuleType(str, Enum):
    SYNC = "sync"  # Is run via a service call
    ASYNC = "async"  # Is executed via gitlab ci


class JobAction(str, Enum):
    PLAY = "play"
    RETRY = "retry"
    DELETE = "delete"
    CANCEL = "cancel"


class JobStatus(str, Enum):
    NOT_SET = ""
    RECEIVED = "RECEIVED"
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETE = "COMPLETE"
    FAILED = "FAILED"


class FileFieldDescription(CamelModel):
    name: str
    description: str
    valid_extensions: List[str]
    max_size: Optional[int] = None
    mandatory: bool = False


class ScidraModule(CamelModel):
    version: str = "1.0.0"
    name: str
    description: str = ""
    module_type: ModuleType = ModuleType.ASYNC
    docker_image: str
    input_schema: str = ""
    output_schema: str = ""
    input_files: List[FileFieldDescription] = []
    cpu_limit: str = "4000m"
    cpu_request: str = "1000m"
    memory_limit_gb: int = 8
    memory_request_gb: int = 2


class JobRun(CamelModel):
    id: int
    workflow_id: int
    status: str = ""
    started_at: Optional[str] = None
    finished_at: Optional[str] = None
    duration: Optional[float] = None
    name: str = ""
    stage: Optional[str] = None
    output: Optional[Union[List, dict]] = None
    files: Optional[List[File]] = None
    log: Optional[bytes] = None
    model_config = ConfigDict(use_enum_values=True)

    def get_compare_time(self) -> datetime:
        if self.started_at is None:
            if self.status not in ["failed", "canceled", "skipped"]:
                return datetime.min.replace(tzinfo=timezone.utc)
            else:
                return datetime.now(tz=timezone.utc)
        else:
            return parser.isoparse(self.started_at)


class WorkflowRun(CamelModel):
    """Equivilant to  gitlab pipeline"""

    id: int
    gitlab_project_id: int
    gitlab_project_branch: str
    commit_id: str
    status: str = ""
    jobs: List[JobRun] = []
    hidden_jobs: Optional[List[JobRun]] = []
    started_at: Optional[str] = None
    finished_at: Optional[str] = None
    duration: Optional[int] = None


# class ScidraJob(CamelModel):
#     id: int
#     module_id: str
#     status: Optional[JobStatus]
#     inputs: dict = {}
#     outputs: dict = {}
#     console: List[str] = []


# class ScidraWorkflow(CamelModel):
#     id: int
#     user_id: str
#     project_id: str
#     workflow_description: str = ""
#     jobs: List[ScidraJob] = []
#     last_run: Optional[WorkflowRun] = None


class WorkflowProject(CamelModel):
    name: str
    user_id: str
    bucket_id: str
    gitlab_project_id: int
    created: Optional[str] = None
    timezone: str = "UTC"

    @field_validator("timezone")
    @classmethod
    def must_be_valid_timezone(cls, v):
        if v not in pytz.all_timezones:
            raise ValueError(f"{v} is not a valid timezone")
        return v
