import logging
from enum import Enum
from typing import List, Optional, Set

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

# from app.shared.utils import auth


class StorageType(str, Enum):
    MINIO = "MINIO"
    GCP_STORAGE = "GCP_STORAGE"
    FIREBASE_STORAGE = "FIREBASE_STORAGE"
    NONE = "NONE"


class DatabaseType(str, Enum):
    MONGODB = "MONGODB"
    GCP_FIRESTORE = "GCP_FIRESTORE"
    NONE = "NONE"


class AuthType(str, Enum):
    OAUTH2 = "OAUTH2"
    STANDALONE = "STANDALONE"


class FACommonSettings(BaseSettings):
    VERSION: str = "2.0.0"
    API_VERSION: int = 1
    API_PRE_PATH: str = f"/api/v{API_VERSION}"

    SECURE: bool = False  # Use secure.py (set to true for prod)
    ROLLBAR_KEY: Optional[str] = None
    ROLLBAR_LOG_LEVEL: int = logging.ERROR
    FA_DEBUG: bool = False
    UNIT_TESTING: bool = False
    ENVIRONMENT: str = "local"

    # SECRET_KEY: SecretBytes = os.urandom(32)  # type:ignore
    BUILD_DATE: Optional[str] = None
    PROJECT_NAME: str = "FastAPI Backend"
    BACKEND_CORS_ORIGINS: Set[str] = set()
    MINIO_SECRET_KEY: Optional[SecretStr] = None
    MINIO_ACCESS_KEY: Optional[str] = None
    MINIO_ENDPOINT: Optional[str] = None
    MINIO_SSL: bool = False

    ENABLE_WORKFLOW: bool = True
    GITLAB_PRIVATE_TOKEN: Optional[str] = None
    GITLAB_GROUP_ID: Optional[int] = None
    GITLAB_URL: Optional[str] = "https://gitlab.com/"
    WORKFLOW_UPLOAD_PATH: str = "job_data"

    BUCKET_NAME: str = ""
    BUCKET_PREFIX: str = ""
    BUCKET_USER_FOLDER: str = "user-storage/"

    AUTH0_DOMAIN: str = ""
    API_AUDIENCE: str = ""
    USE_AUTH0_PROFILE: bool = True
    OAUTH2_AUTH_URL: str = f"https://{AUTH0_DOMAIN}/authorize?audience={API_AUDIENCE}"
    JWT_ALGORITHMS: List[str] = ["RS256"]
    ROLES_NAMESPACE: str = "http://namespace/roles"
    ENABLE_SCOPES: bool = True

    AUTH_TYPE: AuthType = AuthType.OAUTH2

    # logging configuration
    LOGGING_LEVEL: int = logging.DEBUG if FA_DEBUG else logging.INFO

    DATABASE_TYPE: DatabaseType = DatabaseType.GCP_FIRESTORE  # FIRESTORE or MONGODB
    STORAGE_TYPE: StorageType = StorageType.GCP_STORAGE
    USE_FIREBASE: bool = (
        STORAGE_TYPE == StorageType.FIREBASE_STORAGE or DATABASE_TYPE == DatabaseType.GCP_FIRESTORE
    )

    MONGODB_DSN: Optional[str] = None
    MONGODB_DBNAME: Optional[str] = None
    USE_BEANIE: bool = False
    MONGO_AUTO_CONNECT: bool = True
    mongodb_min_pool_size: int = 0
    mongodb_max_pool_size: int = 100
    TZ: str = "UTC"
    APP_PATH: str = "fa_common"
    FASTAPI_APP: str = ""

    debug_timing: bool = False
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings: Optional[FACommonSettings] = None


def get_settings(env_path=None) -> FACommonSettings:
    # Load env variables from .env file

    global settings
    if settings is None or env_path is not None:
        settings = FACommonSettings(_env_file=env_path)  # type: ignore

    return settings
