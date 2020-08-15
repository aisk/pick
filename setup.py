#-*-coding:utf-8-*-

import os
from setuptools import setup

def fread(fname):
    filepath = os.path.join(os.path.dirname(__file__), fname)
    with open(filepath, 'r') as fp:
        return fp.read()

setup(
    name='pick',
    version='0.6.7',
    description='pick an option in the terminal with a simple GUI',
    long_description=fread('README.rst'),
    keywords='terminal gui',
    url='https://github.com/wong2/pick',
    author='wong2',
    author_email='wonderfuly@gmail.com',
    license='MIT',
    packages=['pick'],
    install_requires=['windows-curses; platform_system=="Windows"'],
    tests_require=['nose'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
    ]
)
