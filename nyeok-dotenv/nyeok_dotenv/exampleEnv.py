from enum import Enum
from .EnvBase import EnvBase


class MyEnv[ModeT: Enum](EnvBase[ModeT]):
    # You should Write all environment variables here
    # .env
    POSTGRES_USER: str
    # .secret
    POSTGRES_PASSWORD: str


class MyMode(Enum):
    # Enum name is used in code
    # Enum value is used to be set in Dockerfile
    PROD = "prod"
    DEV = "dev"


# use-site Env.py와 같은 디렉토리를 read하는 것을 보장해야 한다.
env = MyEnv(
    # Set as "ENV APP_ENV=prod" in Dockerfile
    configs={
        MyMode.PROD: [".env.prod"],  # .secret is loaded by env in k8s
        MyMode.DEV: [".env.dev", ".secret"],
    },
    env_variable_for_mode="APP_ENV",
)

print(env)
