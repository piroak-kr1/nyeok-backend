from enum import StrEnum
import os

from nyeok_dotenv.EnvBase import load_enum_from_environment_by_value
import pytest


class MyEnum(StrEnum):
    A = "a"
    B = "b"
    C = "c"


def test_good_case():
    os.environ["MY_ENUM"] = MyEnum.B.value

    result = load_enum_from_environment_by_value(
        available_enums=MyEnum,
        env_variable_key="MY_ENUM",
    )
    assert result == MyEnum.B


def test_default_value():
    # Do not set MY_ENUM
    result = load_enum_from_environment_by_value(
        available_enums=MyEnum,
        env_variable_key="MY_ENUM",
        default_value=MyEnum.C,
    )
    assert result == MyEnum.C


def test_no_env_without_default():
    # Do not set MY_ENUM
    with pytest.raises(Exception) as e:
        load_enum_from_environment_by_value(
            available_enums=MyEnum,
            env_variable_key="MY_ENUM",
        )
    assert str(e.value) == 'There is no "MY_ENUM" in os.environ'


def test_bad_value_with_default():
    os.environ["MY_ENUM"] = "d"

    result = load_enum_from_environment_by_value(
        available_enums=MyEnum,
        env_variable_key="MY_ENUM",
        default_value=MyEnum.C,
    )
    assert result == MyEnum.C


def test_bad_value_without_default():
    os.environ["MY_ENUM"] = "d"

    with pytest.raises(ValueError) as e:
        load_enum_from_environment_by_value(
            available_enums=MyEnum,
            env_variable_key="MY_ENUM",
        )
    assert str(e.value) == '"d" does not exist in available_enums.value'
