import os
import typing
from dotenv import load_dotenv


class Env:
    # Write all environment variables here
    # .env
    # .secret
    DATAKR_API_KEY: str

    def __init__(self) -> None:
        # Load files in same directory with this file
        original_cwd = os.getcwd()
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

        self.read_files_to_os()
        self.set_env_from_os()

        os.chdir(original_cwd)

    def read_files_to_os(self) -> None:
        # load_dotenv(".env.prod")
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
