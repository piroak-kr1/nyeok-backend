from enum import StrEnum, unique

from nyeok_dotenv.EnvBase import EnvBase


@unique
class SimpleRuntimeType(StrEnum):
    PROD = "prod"
    DEV = "dev"


class SimpleEnv(EnvBase[SimpleRuntimeType]):
    POSTGRES_USER: str
