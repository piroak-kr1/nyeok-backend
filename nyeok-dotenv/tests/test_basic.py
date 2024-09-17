import os
from .SampleClass import SampleEnv, RuntimeType


def get_env() -> SampleEnv:
    # Helper function for most of the tests
    return SampleEnv(
        files_to_load={
            RuntimeType.PROD: [".env.prod"],  # .secret is loaded by env in k8s
            RuntimeType.STAGE: [".env.stage", ".secret"],
            RuntimeType.DEV: [".env.dev", ".secret"],
        },
        directory=os.path.dirname(__file__),
        env_variable_for_type="RUNTIME_TYPE",
        default_type=None,
    )


def test_environ_empty_before():
    assert "RUNTIME_TYPE" not in os.environ


def test_dev():
    os.environ["RUNTIME_TYPE"] = RuntimeType.DEV.value
    env = get_env()

    assert env.POSTGRES_USER == "username-dev"
    assert env.POSTGRES_PASSWORD == "password1234"


def test_prod():
    os.environ["RUNTIME_TYPE"] = RuntimeType.PROD.value
    os.environ["POSTGRES_PASSWORD"] = "password1234"
    env = get_env()

    assert env.POSTGRES_USER == "username-prod"
    assert env.POSTGRES_PASSWORD == "password1234"


def test_environ_empty_after():
    assert "RUNTIME_TYPE" not in os.environ
