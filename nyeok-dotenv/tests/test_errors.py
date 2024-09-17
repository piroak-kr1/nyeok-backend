from enum import StrEnum
import os
import pytest

from .SimpleClass import SimpleRuntimeType, SimpleEnv


def test_both_env_variable_and_default_type_is_not_set():
    with pytest.raises(ValueError) as e:
        SimpleEnv(
            files_to_load={
                SimpleRuntimeType.PROD: [
                    ".env.prod",
                ],
                SimpleRuntimeType.DEV: [
                    ".env.dev",
                ],
            },
            directory=os.path.dirname(__file__),
            env_variable_for_type=None,
            default_type=None,
        )

    assert str(e.value) == "You should set either env_variable_for_type or default_type"


def test_env_file_not_found():
    with pytest.raises(FileNotFoundError) as e:
        SimpleEnv(
            files_to_load={
                SimpleRuntimeType.PROD: [
                    ".env.not-exist",
                ],
                SimpleRuntimeType.DEV: [
                    ".env.dev",
                ],
            },
            directory=os.path.dirname(__file__),
            default_type=SimpleRuntimeType.PROD,
        )

    assert (
        str(e.value)
        == f"file='.env.not-exist' does not exist in directory='{os.path.dirname(__file__)}'"
    )


def test_attribute_not_found():
    class ComplexEnv(SimpleEnv):
        NON_EXIST_VARIABLE: str

    with pytest.raises(Exception) as e:
        ComplexEnv(
            files_to_load={
                SimpleRuntimeType.PROD: [
                    ".env.prod",
                ],
                SimpleRuntimeType.DEV: [
                    ".env.dev",
                ],
            },
            directory=os.path.dirname(__file__),
            default_type=SimpleRuntimeType.PROD,
        )

    assert str(e.value) == "Missing key='NON_EXIST_VARIABLE' in os.environ"


@pytest.mark.skip
def test_missing_runtime_type():
    os.environ["RUNTIME_TYPE"] = "prod"
    with pytest.raises(ValueError) as e:
        SimpleEnv(
            files_to_load={
                SimpleRuntimeType.PROD: [
                    ".env.prod",
                ],
            },
            directory=os.path.dirname(__file__),
            env_variable_for_type="RUNTIME_TYPE",
        )

    assert str(e.value) == '"prod" does not exist in available_enums.value'


@pytest.mark.skip
def test_runtime_type_with_overlapping_value():
    class SameValueRuntimeType(StrEnum):
        PROD = "prod"
        STAGE = "prod"

    with pytest.raises(ValueError) as e:
        SimpleEnv(
            files_to_load={
                SameValueRuntimeType.PROD: [
                    ".env.prod",
                ],
                SameValueRuntimeType.STAGE: [
                    ".env.stage",
                ],
            },
            directory=os.path.dirname(__file__),
            env_variable_for_type="RUNTIME_TYPE",
        )

    assert (
        str(e.value)
        == "All values of `RuntimeTypeT` should be different from each other."
    )
