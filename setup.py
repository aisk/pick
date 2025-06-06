import os
import sysconfig
from setuptools import setup, find_packages

# Read version and other metadata from pyproject.toml if needed
__version__ = "2.4.0"

install_requires = []

# Check if we're in MSYS2 environment
is_msys2 = (
    sysconfig.get_platform().startswith("mingw") or 
    os.environ.get("MSYSTEM") is not None
)

# Only include windows-curses if we're on Windows but NOT in MSYS2
if os.name == "nt" and not is_msys2:
    install_requires.append("windows-curses >= 2.2.0")

setup(
    name="pick",
    version=__version__,
    description="Pick an option in the terminal with a simple GUI",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="wong2, AN Long",
    author_email="wonderfuly@gmail.com",
    license="MIT",
    url="https://github.com/aisk/pick",
    keywords=["terminal", "gui"],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.7",
    install_requires=install_requires,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers", 
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Shells",
        "Topic :: Terminals",
    ],
)