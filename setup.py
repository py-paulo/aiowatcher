import setuptools
from importlib.machinery import SourceFileLoader
from os import path

from setuptools import setup


module = SourceFileLoader(
    fullname="version", path=path.join("aiowatch", "version.py"),
).load_module()

libraries = []

setuptools.setup(
    name="aiowatch",
    version=module.__version__,
    packages=["aiowatch"],
    license=module.package_license,
    description=module.package_info,
    author=module.__author__,
    author_email=module.team_email,
    keywords=["aio", "python", "asyncio", "fileio", "io"],
    provides=["aiowatch"],
    long_description=open("README.rst").read(),
    url="https://github.com/pypa/sampleproject",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=["aiofile~=3.1.0"],
)

