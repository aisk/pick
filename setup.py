import sysconfig
from setuptools import setup, find_packages

install_requires = []

if not sysconfig.get_platform().startswith("mingw"):
    install_requires.append('windows-curses>=2.2.0,<3.0.0; platform_system == "Windows"')

setup(
    name='pick',
    version='2.5.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=install_requires,
    description="Pick an option in the terminal with a simple GUI",
    author="wong2",
    author_email="wonderfuly@gmail.com",
    license="MIT",
    url="https://github.com/aisk/pick",
    keywords=["terminal", "gui"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Terminals"
    ],
)
