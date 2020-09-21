import setuptools
from importlib.machinery import SourceFileLoader
from os import path

from setuptools import setup


module = SourceFileLoader(
    fullname="version", path=path.join("aiowatcher", "version.py"),
).load_module()

libraries = []

setuptools.setup(
    name="aiowatcher",
    version=module.__version__,
    packages=["aiowatcher"],
    license=module.package_license,
    description=module.package_info,
    author=module.__author__,
    author_email=module.team_email,
    keywords=["aio", "python", "asyncio", "fileio", "io"],
    provides=["aiowatcher"],
    long_description=open("README.rst").read(),
    url="https://github.com/py-paulo/aiowatcher.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=["aiofile~=3.1.0"],
)
