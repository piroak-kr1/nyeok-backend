from enum import StrEnum

from nyeok_dotenv.EnvBase import EnvBase


class RuntimeType(StrEnum):
    # Enum name is used in code
    # Enum value is used to be set as environment variable value
    PROD = "prod"
    STAGE = "staging"
    DEV = "dev"


class SampleEnv(EnvBase[RuntimeType]):
    # You should Write all environment variables here
    # .env
    POSTGRES_USER: str
    # .secret
    POSTGRES_PASSWORD: str
