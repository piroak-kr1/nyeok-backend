# 1. Test for dir1/dir2
# 2. Test for changing cwd (root, dir1)

import os
from pytest import MonkeyPatch

from .SimpleClass import SimpleRuntimeType, SimpleEnv


def get_env_dir1() -> SimpleEnv:
    # Set directory to 'dir1' under the current test file directory
    dir1_path = os.path.join(os.path.dirname(__file__), "dir1")

    return SimpleEnv(
        files_to_load={
            SimpleRuntimeType.PROD: [".env.prod"],
            SimpleRuntimeType.DEV: [".env.dev"],
        },
        directory=dir1_path,
        env_variable_for_type="RUNTIME_TYPE",
        default_type=None,
    )


def get_env_dir2() -> SimpleEnv:
    # Set directory to 'dir2' under the current test file directory
    dir2_path = os.path.join(os.path.dirname(__file__), "dir2")

    return SimpleEnv(
        files_to_load={
            SimpleRuntimeType.PROD: [".env.prod"],
            SimpleRuntimeType.DEV: [".env.dev"],
        },
        directory=dir2_path,
        env_variable_for_type="RUNTIME_TYPE",
        default_type=None,
    )


def test_dir1_prod():
    os.environ["RUNTIME_TYPE"] = SimpleRuntimeType.PROD.value
    env = get_env_dir1()

    assert env.POSTGRES_USER == "username-prod1"


def test_dir1_dev():
    os.environ["RUNTIME_TYPE"] = SimpleRuntimeType.DEV.value
    env = get_env_dir1()

    assert env.POSTGRES_USER == "username-dev1"


def test_dir2_prod():
    os.environ["RUNTIME_TYPE"] = SimpleRuntimeType.PROD.value
    env = get_env_dir2()

    assert env.POSTGRES_USER == "username-prod2"


def test_dir2_dev():
    os.environ["RUNTIME_TYPE"] = SimpleRuntimeType.DEV.value
    env = get_env_dir2()

    assert env.POSTGRES_USER == "username-dev2"


def get_env_current_dir() -> SimpleEnv:
    return SimpleEnv(
        files_to_load={
            SimpleRuntimeType.PROD: [".env.prod"],
            SimpleRuntimeType.DEV: [".env.dev"],
        },
        directory=None,
        env_variable_for_type="RUNTIME_TYPE",
        default_type=None,
    )


def test_env_cwd_root(monkeypatch: MonkeyPatch):
    monkeypatch.chdir(os.path.dirname(__file__))

    os.environ["RUNTIME_TYPE"] = SimpleRuntimeType.PROD.value
    env = get_env_current_dir()

    assert env.POSTGRES_USER == "username-prod"


def test_env_cwd_dir1(monkeypatch: MonkeyPatch):
    monkeypatch.chdir(os.path.join(os.path.dirname(__file__), "dir1"))

    os.environ["RUNTIME_TYPE"] = SimpleRuntimeType.DEV.value
    env = get_env_current_dir()

    assert env.POSTGRES_USER == "username-dev1"
