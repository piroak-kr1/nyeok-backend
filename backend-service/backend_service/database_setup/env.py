from enum import StrEnum, unique
import os
from nyeok_dotenv.EnvBase import EnvBase


@unique
class BuildTypes(StrEnum):
    PROD = "prod"
    DEV = "dev"


class AppEnv(EnvBase[BuildTypes]):
    # .env
    # .secret
    DATAKR_API_KEY: str


# exported
env = AppEnv(
    runtime_type_cls=BuildTypes,
    files_to_load={
        BuildTypes.PROD: [],  # secret will be loaded by k8s
        BuildTypes.DEV: [".secret"],
    },
    directory=os.path.dirname(__file__),  # directory of this file
    env_variable_for_type="BUILD_TYPE",
    default_type=BuildTypes.DEV,
)
print(env)
