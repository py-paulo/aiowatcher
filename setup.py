import setuptools
from importlib.machinery import SourceFileLoader
from os import path
import sys
import pathlib


if sys.version_info < (3, 6):
    raise RuntimeError("aiohttp 4.x requires Python 3.6+")

HERE = pathlib.Path(__file__).parent
IS_GIT_REPO = (HERE / '.git').exists()

module = SourceFileLoader(
    fullname="version", path=path.join("aiowatcher", "version.py"),
).load_module()

libraries = []

def read(f):
    return (HERE / f).read_text('utf-8').strip()

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
    long_description='\n\n'.join((read('README.md'), read('CHANGES.md'))),
    long_description_content_type='text/markdown',
    url="https://github.com/py-paulo/aiowatcher.git",
    classifiers=[
        "Environment :: Console",
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Framework :: AsyncIO',
    ],
    project_urls={
        'GitHub: issues': 'https://github.com/py-paulo/aiowatcher/issues',
        'GitHub: repo': 'https://github.com/py-paulo/aiowatcher',
    },
    python_requires='>=3.6',
    install_requires=["aiofile~=3.1.0"],
)
