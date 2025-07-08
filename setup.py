from setuptools import setup, Extension, find_packages
from setuptools.command.build_ext import build_ext
import subprocess
import sys
import os


class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=""):
        super().__init__(name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)


class CMakeBuild(build_ext):
    def run(self):
        for ext in self.extensions:
            self.build_cmake(ext)
        super().run()

    def build_cmake(self, ext):
        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
        cmake_args = [
            f"-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={extdir}",
            f"-DPYTHON_EXECUTABLE={sys.executable}",
            "-DCMAKE_BUILD_TYPE=Release",
        ]

        build_temp = self.build_temp
        os.makedirs(build_temp, exist_ok=True)

        subprocess.check_call(["cmake", ext.sourcedir] + cmake_args, cwd=build_temp)
        subprocess.check_call(["cmake", "--build", "."], cwd=build_temp)


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="phantomroll",
    version="1.0.0",
    author="Nyakeriga",
    author_email="you@example.com",
    description="Stealth Telegram Dice Control Tool - 幽影掷点",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nyakeriga/phantomroll",
    project_urls={
        "Bug Tracker": "https://github.com/nyakeriga/phantomroll/issues",
        "Documentation": "https://github.com/nyakeriga/phantomroll/wiki"
    },
    packages=find_packages(),
    include_package_data=True,
    ext_modules=[CMakeExtension("phantomcore")],
    cmdclass={"build_ext": CMakeBuild},
    install_requires=[
        "telethon>=1.34.0",
        "py-cpuinfo",
        "psutil",
        "PyQt5",
        "websockets"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: C++",
        "Programming Language :: Java",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Communications :: Chat",
        "Topic :: Security",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "phantomroll=phantomroll.cli:main",
        ],
    },
)
