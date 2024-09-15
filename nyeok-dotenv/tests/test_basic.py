import os
from .SampleClass import SampleEnv, RuntimeType


def test_dev():
    os.environ["RUNTIME_TYPE"] = RuntimeType.DEV.value
    env = SampleEnv(
        files_to_load={
            RuntimeType.PROD: [".env.prod"],  # .secret is loaded by env in k8s
            RuntimeType.STAGE: [".env.stage", ".secret"],
            RuntimeType.DEV: [".env.dev", ".secret"],
        },
        directory=os.path.dirname(__file__),
        env_variable_for_type="RUNTIME_TYPE",
        default_type=None,
    )

    assert env.POSTGRES_USER == "username-dev"
    assert env.POSTGRES_PASSWORD == "password1234"
