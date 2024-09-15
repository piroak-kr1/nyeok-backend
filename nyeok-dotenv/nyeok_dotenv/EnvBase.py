from enum import Enum, StrEnum
import os
import typing
from typing import Any, Iterable
from dotenv import load_dotenv
from .DirecoryChanger import DirectoryChanger


def find_enum_by_value[
    EnumT: Enum
](enums: Iterable[EnumT], enum_value: Any) -> EnumT | None:
    """
    Finds an enum member by its value from a collection of enum members.

    This function takes an iterable of enum members and a value. It returns the first enum member
    whose `.value` matches the provided value. If no match is found, it returns `None`.

    Args:
        enums (Iterable[EnumT]): An iterable collection of enum members to search.
        enum_value (Any): The value to match against the `.value` attribute of the enum members.

    Returns:
        EnumT | None: The first enum member whose `.value` equals `enum_value`, or `None` if no match is found.

    Example:
        class Color(Enum):
            RED = 1
            BLUE = 2
            GREEN = 3

        color = find_by_enum_value(Color, 2)
        # Returns: Color.BLUE
    """
    single_result: filter[EnumT] = filter(lambda x: x.value == enum_value, enums)
    return next(single_result, None)


def load_enum_from_environment_by_value[
    EnumT: StrEnum
](
    available_enums: Iterable[EnumT],
    env_variable_key: str,
    default_value: EnumT | None = None,
) -> EnumT:
    """
    Loads an enum from an environment variable.

    This function retrieves a value from the environment using the specified
    environment variable name, then matches it with one of the provided enums
    by comparing the value to the `value` attribute of each enum. If no match
    is found and no default is provided, it raises an error.

    Args:
        available_enums (Iterable[EnumT]): A collection of enum members to search.
        env_variable_key (str): The name of the environment variable to fetch the enum.
        default_value (EnumT | None): The default enum to return if no match is found.
            If not provided and the value doesn't match any enum, an error is raised.

    Returns:
        EnumT: The matched enum member based on the value of the environment variable.

    Raises:
        Exception: If the specified environment variable is not set.
        ValueError: If the value retrieved from the environment variable does not match any
            of the available enum members and no default is provided.
    """

    # Try search_result.value == os.environ[env_variable_key]
    try:
        mode_str = os.environ[env_variable_key]
    except KeyError:
        mode_str = None
    search_result: EnumT | None = (
        find_enum_by_value(available_enums, mode_str) if mode_str is not None else None
    )

    if search_result is not None:
        return search_result
    if default_value is not None:
        return default_value
    if mode_str is None:
        raise Exception(f'There is no "{env_variable_key}" in os.environ')
    else:  # mode_str is not None, but search_result is None
        raise ValueError(f'"{mode_str}" does not exist for "{EnumT}".value')


class EnvBase[ModeT: StrEnum]:
    _mode: ModeT
    _files_to_load: list[str]

    def __init__(
        self,
        files_to_load: dict[ModeT, list[str]],
        directory: str | None = None,
        env_variable_for_mode: str | None = None,
        default_mode: ModeT | None = None,
    ) -> None:
        """Select mode by `env_variable_for_mode` and load files according to mode.

        :param files_to_load: Dictionary of list of files to load according to ModeT.
        :param directory: Directory where files are located. Use pwd if not set.
        :param env_variable_for_mode: You should set Environment variable `${env_variable_for_mode}` to mode.value in Dockerfile.
        """

        # TODO: Validate configs
        # all value should be different

        # Select Mode
        if env_variable_for_mode is not None:
            # Select mode by reading environment variable
            self._mode = load_enum_from_environment_by_value(
                available_enums=files_to_load.keys(),
                env_variable_key=env_variable_for_mode,
                default_value=default_mode,
            )
        else:
            # If env_variable_for_mode is not set, use default_mode
            if default_mode is None:
                raise ValueError(
                    f"You should set either env_variable_for_mode or default_mode"
                )
            self._mode = default_mode

        # Load files
        self.read_files_to_environment(
            files_to_load=files_to_load[self._mode],
            directory=directory,
        )
        self.set_attr_from_environment()

    def read_files_to_environment(
        self, files_to_load: list[str], directory: str | None
    ) -> None:
        """Read all env files from directory and set os.environ"""
        with DirectoryChanger(directory):
            for file in files_to_load:
                # Check if file exists
                if not os.path.isfile(file):
                    raise FileNotFoundError(f"File {file} does not exist")
                load_dotenv(file)

    def set_attr_from_environment(self) -> None:
        """Read os.environ and set attributes of this class"""

        for key in typing.get_type_hints(self).keys():
            if key.startswith("_"):  # filter some attributes
                continue
            if key not in os.environ:
                raise Exception(f"Missing {key} in os.environ")
            setattr(self, key, os.environ[key])

    def __str__(self) -> str:
        return "\n".join([f"{key}: {value}" for key, value in vars(self).items()])
