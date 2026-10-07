from setuptools import setup
from Cython.Build import cythonize
import numpy as np
import os
import re
import sys
from pathlib import Path
from typing import Dict

from Orbitool.utils.files import FolderTraveler
from tools.build_config import load_config, save_config

MSVC_GUIDANCE = """\
==================================================================
Cannot build the Cython extensions: Microsoft Visual C++ 14 or
greater was not found.

Two options:
  1. Install MSVC Build Tools:
       winget install --id Microsoft.VisualStudio.2022.BuildTools -e \\
         --accept-source-agreements --accept-package-agreements \\
         --override "--quiet --wait --norestart --add Microsoft.VisualStudio.Workload.VCTools --includeRecommended"
     (details: docs/dev/build-environment.md)
  2. Use MinGW-w64 instead: set "mingw_dir" in build-config.json
     (details: docs/dev/build-environment.md)
=================================================================="""


class Node:
    def __init__(self, path):
        self.path = path
        self.ref = set()
        self.refed = set()

def getModelName(path: str):
    name = os.path.split(path)[1]
    return os.path.splitext(name)[0]

def variableIn(variable: str, text: str):
    pattern = r'(\W|^)'+variable+r'(\W|$)'

    for piece in re.finditer(r'[^\n]*import[^\n]*', text):
        piece: re.match
        if re.search(pattern, piece.group()) is not None:
            return True
    return False


def mingwGcc(mingw_dir: str) -> Path:
    return Path(mingw_dir).expanduser() / "bin" / "gcc.exe"


def prepareMingw(mingw_dir: str):
    gcc = mingwGcc(mingw_dir)
    if not gcc.is_file():
        raise RuntimeError(
            f'cannot find "{gcc}" - check "mingw_dir" in build-config.json')
    os.environ["PATH"] = str(
        gcc.parent) + os.pathsep + os.environ.get("PATH", "")


def cythonSetup(filepath, mingw=False):
    cy = cythonize(filepath, annotate=True,
                   compiler_directives={'language_level': 3})
    if mingw:
        # MS_WIN64: MSVC-built pyconfig.h only defines it under _MSC_VER;
        # without it gcc sees SIZEOF_VOID_P=4 and Cython's static assert
        # fails. -static: keep libstdc++/libgcc/winpthread out of the .pyd
        # so it loads on machines without a MinGW runtime.
        for ext in cy:
            ext.define_macros = list(
                ext.define_macros or []) + [("MS_WIN64", "1")]
            ext.extra_link_args = list(ext.extra_link_args or []) + ["-static"]
        script_args = ['build_ext', '--compiler=mingw32']
    else:
        script_args = ['build_ext']
    setup(ext_modules=cy, packages=[], script_args=script_args, include_dirs=[
          np.get_include()], options={'build_ext': {'inplace': True}})


def compileAll(root, mingw=False):
    ft = FolderTraveler(root, '.pyx', True)
    modelNodes: Dict[str, Node]= {}

    for path in ft:
        node = Node(path)
        modelNodes[getModelName(path)] = node

    for model1, node1 in modelNodes.items():
        with open(node1.path, 'r', encoding='utf-8') as f:
            text = f.read()
            for model2, node2 in modelNodes.items():
                if variableIn(model2, text):
                    node1.ref.add(model2)
                    node2.refed.add(model1)
                    
    while len(modelNodes) > 0:
        processed = []

        for model1, node1 in modelNodes.items():
            if len(node1.ref) == 0:
                print(f"process {node1.path}")
                cythonSetup(node1.path, mingw=mingw)
                processed.append(model1)

                for model2 in node1.refed:
                    node2 = modelNodes[model2]
                    node2.ref.remove(model1)

        if len(processed) == 0:
            raise Exception("Loop", modelNodes.keys())
        for pro in processed:
            modelNodes.pop(pro)


def askMingwDir():
    """Print guidance; on a TTY, offer to take a MinGW-w64 directory.

    Returns a validated directory, or None if the user cancelled /
    there is no interactive terminal.
    """
    print(MSVC_GUIDANCE)
    if not sys.stdin.isatty():
        return None
    while True:
        try:
            answer = input(
                'MinGW-w64 directory (e.g. "D:\\tools\\mingw64"), Enter to cancel: '
            ).strip().strip('"')
        except (EOFError, KeyboardInterrupt):
            print()
            return None
        if not answer:
            return None
        if mingwGcc(answer).is_file():
            return answer
        print(f'cannot find "{mingwGcc(answer)}", please try again')


def main(root):
    config, _ = load_config()
    mingw_dir = (config.mingw_dir or "").strip()
    if mingw_dir:
        prepareMingw(mingw_dir)
        print(f"using MinGW-w64: {mingw_dir}")
    try:
        compileAll(root, mingw=bool(mingw_dir))
    except SystemExit as error:
        # distutils converts build failures into SystemExit("error: ...")
        if mingw_dir or "Microsoft Visual C++" not in str(error):
            raise
        answer = askMingwDir()
        if answer is None:
            raise
        config.mingw_dir = answer
        save_config(config)
        print(f'saved mingw_dir to build-config.json, retrying: "{answer}"')
        prepareMingw(answer)
        compileAll(root, mingw=True)

def clear(root):
    ft = FolderTraveler(root, '.pyd', True)
    for path in ft:
        os.remove(path)
