from enum import Enum, StrEnum, unique
import os
from typing import get_type_hints, Any, Iterable
from dotenv import load_dotenv
from .DirecoryChanger import DirectoryChanger


def assert_enum_values_are_unique(enum_class: type[Enum]):
    """
    Ensures that all values in the given Enum class are unique by applying the `@unique` decorator.

    This function attempts to apply the `@unique` decorator to the specified Enum class. The `@unique`
    decorator enforces that all member values in the Enum are distinct. If duplicate values are present,
    it will raise a `ValueError`.

    Args:
        enum_class (type[Enum]): The Enum class to check for unique values.

    Raises:
        ValueError: If any duplicate values are found within the Enum class after applying the `@unique` decorator.
    """

    # Try apply @unique decorator to enum_class
    # NOTE: Maybe @unique decorator is used for enum, but try again
    unique(enum_class)


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
        raise ValueError(f'"{mode_str}" does not exist in available_enums.value')


class EnvBase[RuntimeTypeT: StrEnum]:
    """
    Base class for managing environment configurations based on runtime types.

    This class provides functionality to:
    1. Validate the configuration of environment files to ensure that all runtime types are covered and values are unique.
    2. Select a runtime type based on an environment variable or default value.
    3. Load environment variables from the specified files corresponding to the selected runtime type.
    4. Set class attributes based on the loaded environment variables.

    Attributes:
        _runtimeType (RuntimeTypeT): The runtime type currently selected, determining which environment files to load. (ex) dev, prod)
    """

    _runtimeType: RuntimeTypeT

    def __init__(
        self,
        runtime_type_cls: type[RuntimeTypeT],
        files_to_load: dict[RuntimeTypeT, list[str]],
        directory: str | None = None,
        env_variable_for_type: str | None = None,
        default_type: RuntimeTypeT | None = None,
    ) -> None:
        """
        Initializes the environment configuration.

        This constructor performs the following steps:
        1. Validates that the `files_to_load` dictionary includes all enum members of `runtime_type_cls`
        and that all enum values are unique.
        2. Selects the runtime type based on the provided environment variable or default type.
        3. Loads the environment variables from the specified files for the selected runtime type.
        4. Sets the attributes of the instance based on the loaded environment variables.

        Args:
            runtime_type_cls (type[RuntimeTypeT]): The enum class used to define the runtime types.
            files_to_load (dict[RuntimeTypeT, list[str]]): A dictionary mapping runtime types to lists of file paths.
            directory (str | None, optional): The directory to use for reading the files. Defaults to None.
            env_variable_for_type (str | None, optional): The environment variable used to determine the runtime type. Defaults to None.
            default_type (RuntimeTypeT | None, optional): The default runtime type to use if `env_variable_for_type` is not set. Defaults to None.

        Raises:
            ValueError: If `files_to_load` is invalid or if neither `env_variable_for_type` nor `default_type` is provided.
            Exception: If any issues occur while loading environment variables or setting instance attributes.
        """

        self.validate_files_to_load(runtime_type_cls, files_to_load)

        # Select Runtime Type
        if env_variable_for_type is not None:
            # Select runtime type by reading environment variable
            self._runtimeType = load_enum_from_environment_by_value(
                available_enums=files_to_load.keys(),
                env_variable_key=env_variable_for_type,
                default_value=default_type,
            )
        else:
            # If env_variable_for_type is not set, use default_type
            if default_type is None:
                raise ValueError(
                    f"You should set either env_variable_for_type or default_type"
                )
            self._runtimeType = default_type

        # Load files
        self.read_files_to_environment(
            files_to_load=files_to_load[self._runtimeType],
            directory=directory,
        )
        self.set_attr_from_environment()

    def validate_files_to_load(
        self,
        runtime_type_cls: type[RuntimeTypeT],
        files_to_load: dict[RuntimeTypeT, list[str]],
    ) -> None:
        """
        Validates the configuration of files to load based on the runtime type.

        This method performs two checks:
        1. Ensures that all enum members of `runtime_type_cls` are present as keys
           in the `files_to_load` dictionary.
        2. Verifies that all values of the `runtime_type_cls` enum are unique.

        Args:
            runtime_type_cls (type[RuntimeTypeT]): The enum class that defines the expected runtime types.
            files_to_load (dict[RuntimeTypeT, list[str]]): A dictionary mapping runtime types to lists of file paths.

        Raises:
            ValueError: If `files_to_load` is empty or if any expected enum members are missing from `files_to_load`.
            Exception: If any enum values in `runtime_type_cls` are not unique.
        """

        if not files_to_load:
            raise ValueError(f"files_to_load should not be empty")

        # 1. All enum members of `RuntimeTypeT` should exist in configs.
        #   (This is to avoid non-deterministic errors)

        # Get all members of the Enum class passed in runtime_type_cls
        expected_keys = set(runtime_type_cls)
        actual_keys = set(files_to_load.keys())
        if expected_keys != actual_keys:
            missing_keys = expected_keys - actual_keys
            raise ValueError(
                f"files_to_load must include all instances of {runtime_type_cls}. Missing keys: {missing_keys}"
            )

        # 2. All values of `RuntimeTypeT` should be different from each other.
        #    (We have to determine RuntimeType Enum by value from environment variable)
        assert_enum_values_are_unique(runtime_type_cls)

    def read_files_to_environment(
        self, files_to_load: list[str], directory: str | None
    ) -> None:
        """Read all env files from directory and set os.environ"""

        with DirectoryChanger(directory):
            for file in files_to_load:
                # Check if file exists
                if not os.path.isfile(file):
                    raise FileNotFoundError(f"{file=} does not exist in {directory=}")
                load_dotenv(file)

        # returned to original cwd

    def set_attr_from_environment(self) -> None:
        """Read os.environ and set attributes of this class"""

        # Get type hints from the class hierarchy
        type_hints: dict[str, Any] = {}
        for cls in self.__class__.__mro__:  # Traverse the MRO (method resolution order)
            type_hints.update(get_type_hints(cls))

        # Set attributes from os.environ
        for key in type_hints.keys():
            if key.startswith("_"):  # filter some attributes
                continue
            if key not in os.environ:
                raise Exception(f"Missing {key=} in os.environ")
            setattr(self, key, os.environ[key])

    def __str__(self) -> str:
        """
        Example:
            _runtimeType: dev
            POSTGRES_USER: username-dev
            POSTGRES_PASSWORD: password1234
        """
        return "\n".join([f"{key}: {value}" for key, value in vars(self).items()])
