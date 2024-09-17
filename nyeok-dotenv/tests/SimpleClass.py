from enum import StrEnum

from nyeok_dotenv.EnvBase import EnvBase


class SimpleRuntimeType(StrEnum):
    PROD = "prod"
    DEV = "dev"


class SimpleEnv(EnvBase[SimpleRuntimeType]):
    POSTGRES_USER: str
