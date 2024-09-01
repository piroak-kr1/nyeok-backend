import os
import typing
from dotenv import load_dotenv


class Env:
    # attributes starting with _ are not loaded from os.environ
    _isProd: bool
    _isDev: bool
    # Write all environment variables here
    # .env
    POSTGRES_HOST: str
    # .secret
    GCP_API_KEY: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str  # TODO: change password

    def __init__(self) -> None:
        self._isProd = "ENV" in os.environ and os.environ["ENV"] == "production"
        self._isDev = not self._isProd

        # Load files in same directory with this file
        original_cwd = os.getcwd()
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

        self.read_files_to_os()
        self.set_env_from_os()

        os.chdir(original_cwd)

    def read_files_to_os(self) -> None:
        if self._isProd:
            load_dotenv(".env.prod")
            # NOTE: secret is already injected to env with k8s pod spec
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
