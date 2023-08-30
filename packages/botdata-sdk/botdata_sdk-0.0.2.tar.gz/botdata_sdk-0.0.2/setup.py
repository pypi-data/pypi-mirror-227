import sys
import subprocess
from setuptools import setup, Extension, find_packages
from setuptools.command.build_ext import build_ext
from distutils.spawn import find_executable

# Check if Bazel is installed
if find_executable("bazel") is None:
    print("Bazel is not installed. Please install Bazel and make it available in PATH.")
    sys.exit(1)

# Define the Extension module
ext_module = Extension(
    'botdata_sdk',  # Name of the resulting Python module
    sources=[],  # No need to specify sources here, as they're handled by Bazel
    include_dirs=['python/bind'],  # Include directories
    language='c++'
)

# Subclass build_ext to customize the build process
class BuildExt(build_ext):
    def run(self):
        # Use Bazel to build the C++ extension
        subprocess.run(["bazel", "build", "//python/bind:botdata_sdk_wrapper"])

# Setup configuration
setup(
    packages=find_packages(),
    ext_modules=[ext_module],  # List of extension modules
    cmdclass={'build_ext': BuildExt},  # Use the custom build_ext class
)
