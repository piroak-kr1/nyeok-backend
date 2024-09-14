from enum import Enum
import os
import typing
from typing import Any, Iterable
from dotenv import load_dotenv


def find_by_enum_value[
    EnumT: Enum
](enums: Iterable[EnumT], enum_value: Any) -> EnumT | None:
    """Search enums according to enum.value"""
    single_result: filter[EnumT] = filter(lambda x: x.value == enum_value, enums)
    return next(single_result, None)


class EnvBase[ModeT: Enum]:
    _mode: ModeT
    _files_to_load: list[str]

    def __init__(
        self,
        configs: dict[ModeT, list[str]],
        env_variable_for_mode: str | None = None,
        default_mode: ModeT | None = None,
    ) -> None:
        """Select mode by `env_variable_for_mode` and load files according to mode.

        :param configs: Dictionary of list of files to load according to ModeT.
        :param env_variable_for_mode: You should set Environment variable `${env_variable_for_mode}` to mode.value in Dockerfile.
        """

        # TODO: Validate configs

        # Select mode by reading environment variable
        self._mode = self.choose_mode(
            available_modes=configs.keys(),
            env_variable_for_mode=env_variable_for_mode,
            default_mode=default_mode,
        )
        self._files_to_load = configs[self._mode]

        # Load files in same directory with this file
        original_cwd = os.getcwd()
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

        self.read_files_to_os()
        self.set_env_from_os()

        os.chdir(original_cwd)

    def choose_mode(
        self,
        available_modes: Iterable[ModeT],
        env_variable_for_mode: str | None = None,
        default_mode: ModeT | None = None,
    ) -> ModeT:
        """Choose mode by reading environment variable.

        :param available_modes: List of all available modes.
        :param env_variable_for_mode: Environment variable name for mode selection.
        :param default_mode: Default mode if environment variable is not set.
        """

        # If env variable is not set, use default mode
        if env_variable_for_mode is None:
            if default_mode is None:
                raise ValueError(
                    f"You should set either env_variable_for_mode or default_mode"
                )
            return default_mode

        # Otherwise, read env varaiable
        try:
            mode_str = os.environ[env_variable_for_mode]
        except KeyError:
            raise Exception(f'There is no "{env_variable_for_mode}" in os.environ')

        search_result = find_by_enum_value(available_modes, mode_str)
        if search_result is None:
            raise ValueError(f'"{mode_str}" does not exists for "{ModeT}".value')

        return search_result

    def read_files_to_os(self) -> None:
        """Read all env files and set os.environ"""

        for file in self._files_to_load:
            # TODO: check if file exists
            load_dotenv(file)

    def set_env_from_os(self) -> None:
        """Read os.environ and set attributes of this class"""

        for key in typing.get_type_hints(self).keys():
            if key.startswith("_"):  # filter some attributes
                continue
            if key not in os.environ:
                raise Exception(f"Missing {key} in os.environ")
            setattr(self, key, os.environ[key])

    def __str__(self) -> str:
        # TODO:
        return "\n".join([f"{key}: {value}" for key, value in vars(self).items()])
