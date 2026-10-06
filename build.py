import os
from pathlib import Path
import subprocess
from traceback import print_exc
import zipfile

import pytest

from Orbitool.version import VERSION
from utils import pyuic, setup
from utils.build_config import Config, read_config

try:
    import jedi
    assert False, "You should build in build environment"
except AssertionError:
    raise
except:
    pass


CWD = Path.cwd()
DIST_DIR = Path("dist")
EXE_DIR = DIST_DIR / "Orbitool"
ZIP_PATH = DIST_DIR / \
    f"Orbitool-{VERSION.replace('.','_')}.zip"


def run_pyuic(config: Config):
    pyuic.pyuic(CWD / "Orbitool/UI")


def run_compile(config: Config):
    try:
        for pyd in (CWD / "Orbitool").glob("**/*.pyd"):
            print("removing pyd", pyd)
            pyd.unlink()
        setup.main(CWD / "Orbitool")
    except:
        print_exc()
        return False
    return True


def run_test(config: Config):
    ret = pytest.main(["-c", "pytest.ini"])
    if ret != 0:
        print(f"pytest FAILED (exit {int(ret)}) - packaging stopped")
        return False
    print("pytest: OK (exit 0)")
    return True


def run_build(config: Config):
    if not config.upx_dir or not Path(config.upx_dir).exists():
        if not config.upx_dir:
            print("please provide upx path")
        else:
            print("cannot find upx path", config.upx_dir)
        return False
    os.system(f"pyinstaller main.spec --upx-dir {config.upx_dir} -y")
    return True


def run_package(config: Config):
    count = 0
    with zipfile.ZipFile(ZIP_PATH, 'w') as file:
        for path in EXE_DIR.glob("**/*"):
            file.write(path, path.relative_to(DIST_DIR), zipfile.ZIP_DEFLATED)
            count += 1
    print(f"packaged {count} files into {ZIP_PATH}")

    subprocess.Popen(
        f'explorer /select,"{ZIP_PATH.absolute()}"')


if __name__ == "__main__":
    exists, config = read_config()
    if not exists:
        print("build-config.json was created, please check it\n and rerun this script to continue")
        exit()
    if config.compile:
        run_pyuic(config)
        if not run_compile(config):
            exit(-1)
    if config.test:
        if not run_test(config):
            exit(-1)
    if config.build:
        if not run_build(config):
            exit(-1)
    if config.zip_file:
        run_package(config)
