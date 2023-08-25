import sys
from unittest.mock import patch

from Cython.Build import cythonize
from hatchling.builders.hooks.plugin.interface import BuildHookInterface
from setuptools import Extension, setup

COMPILEARGS = ["-O2"]
DIRECTIVES = {"binding": True, "language_level": 3}


def build():
    exts = [Extension("*", ["src/funcclasses/**/*.pyx"], extra_compile_args=COMPILEARGS)]
    ext_modules = cythonize(exts, compiler_directives=DIRECTIVES)
    setup(ext_modules=ext_modules)


class CythonBuildHook(BuildHookInterface):
    PLUGIN_NAME = "cython"

    def initialize(self, version: str, build_data: dict):  # noqa: ARG002
        sys.path.append(self.root)
        with patch.object(
            sys,
            "argv",
            [
                "hatch_build.py",
                "build_ext",
                "--inplace",
            ],
        ):
            build()
