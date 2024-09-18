import os
from types import TracebackType


class DirectoryChanger:
    """A context manager that changes working directory, then returns to original cwd."""

    def __init__(self, path: str | None):
        self.path = path

    def __enter__(self):
        self.original_cwd = os.getcwd()
        if self.path is not None:
            os.chdir(os.path.abspath(self.path))

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ):
        # Return to original cwd, even if path is not set
        os.chdir(self.original_cwd)
