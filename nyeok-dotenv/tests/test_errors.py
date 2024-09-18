from enum import StrEnum, unique
import os
from nyeok_dotenv.EnvBase import assert_enum_values_are_unique
import pytest

from .SimpleClass import SimpleRuntimeType, SimpleEnv


def test_both_env_variable_and_default_type_is_not_set():
    with pytest.raises(ValueError) as e:
        SimpleEnv(
            runtime_type_cls=SimpleRuntimeType,
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


def test_empty_files_to_load():
    with pytest.raises(ValueError) as e:
        SimpleEnv(
            runtime_type_cls=SimpleRuntimeType,
            files_to_load={},
            directory=os.path.dirname(__file__),
            default_type=SimpleRuntimeType.PROD,
        )

    assert str(e.value) == "files_to_load should not be empty"


def test_env_file_not_found():
    with pytest.raises(FileNotFoundError) as e:
        SimpleEnv(
            runtime_type_cls=SimpleRuntimeType,
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
            runtime_type_cls=SimpleRuntimeType,
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


def test_missing_runtime_type():
    os.environ["RUNTIME_TYPE"] = SimpleRuntimeType.PROD.value
    with pytest.raises(ValueError) as e:
        SimpleEnv(
            runtime_type_cls=SimpleRuntimeType,
            files_to_load={
                SimpleRuntimeType.PROD: [
                    ".env.prod",
                ],
            },
            directory=os.path.dirname(__file__),
            env_variable_for_type="RUNTIME_TYPE",
        )

    assert (
        str(e.value)
        == "files_to_load must include all instances of <enum 'SimpleRuntimeType'>. Missing keys: {<SimpleRuntimeType.DEV: 'dev'>}"
    )


def test_uniqueness_of_runtime_type_values():
    assert_enum_values_are_unique(SimpleRuntimeType)

    # By unique decorator
    with pytest.raises(ValueError) as e:

        @unique
        class SameValueRuntimeType2(StrEnum):  # type: ignore[no-access]
            PROD = "prod"
            DEV = "prod"

    assert (
        str(e.value)
        == "duplicate values found in <enum 'SameValueRuntimeType2'>: DEV -> PROD"
    )

    # By assert_enum_values_are_unique
    with pytest.raises(ValueError) as e:

        class SameValueRuntimeType(StrEnum):
            PROD = "prod"
            DEV = "prod"

        assert_enum_values_are_unique(SameValueRuntimeType)

    assert (
        str(e.value)
        == "duplicate values found in <enum 'SameValueRuntimeType'>: DEV -> PROD"
    )
