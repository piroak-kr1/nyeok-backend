from enum import StrEnum
import os
from nyeok_dotenv.EnvBase import EnvBase


class RuntimeType(StrEnum):
    # Enum name is used in code
    # Enum value is used to be set as environment variable value
    PROD = "prod"
    DEV = "dev"


class SampleEnv(EnvBase[RuntimeType]):
    # You should Write all environment variables here
    # .env
    POSTGRES_USER: str
    # .secret
    POSTGRES_PASSWORD: str


os.environ["RUNTIME_TYPE"] = RuntimeType.DEV.value
env = SampleEnv(
    files_to_load={
        RuntimeType.PROD: [".env.prod"],  # .secret is loaded by env in k8s
        RuntimeType.DEV: [".env.dev", ".secret"],
    },
    directory=os.path.dirname(__file__),
    env_variable_for_type="RUNTIME_TYPE",
)
