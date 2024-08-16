import os
import typing
from dotenv import load_dotenv


class Env:
    # attributes starting with _ are not loaded from os.environ
    _isProd: bool
    _isDev: bool
    # Write all environment variables here
    # .env
    # .secret
    GCP_API_KEY: str

    def __init__(self) -> None:
        self._isProd = "ENV" in os.environ and os.environ["ENV"] == "production"
        self._isDev = not self._isProd

        self.read_files_to_os()
        self.set_env_from_os()

    def read_files_to_os(self) -> None:
        if self._isProd:
            load_dotenv(".env.prod")
        else:
            load_dotenv(".env.dev")

        load_dotenv(".secret")

    def set_env_from_os(self) -> None:
        for key in typing.get_type_hints(self).keys():
            if key.startswith("_"):  # filter some attributes
                continue
            if key not in os.environ:
                raise Exception(f"Missing {key} in os.environ")
            setattr(self, key, os.environ[key])

    def __str__(self) -> str:
        return "\n".join([f"{key}: {value}" for key, value in vars(self).items()])


# exported
env = Env()
print(env)
