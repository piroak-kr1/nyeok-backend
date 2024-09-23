from enum import StrEnum
import os
from nyeok_dotenv.EnvBase import EnvBase


class RuntimeType(StrEnum):
    PROD = "prod"
    DEV = "dev"


class AppEnv(EnvBase[RuntimeType]):
    # .env
    POSTGRES_HOST: str
    # .secret
    GCP_API_KEY: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str  # TODO: change password


# exported
env = AppEnv(
    runtime_type_cls=RuntimeType,
    env_variable_for_type="RUNTIME_TYPE",
    directory=os.path.dirname(__file__),
    files_to_load={
        RuntimeType.PROD: [".env.prod"],
        RuntimeType.DEV: [".env.dev", ".secret"],
    },
)
print(env)
