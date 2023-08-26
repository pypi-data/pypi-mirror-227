import setuptools
import re
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = ''
with open('central50/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)
if not version:
    raise RuntimeError('Cannot find version information')


with open("README.md", "rb") as f:
    readme = f.read().decode('utf-8')

setup(
    name="central50",
    version=version,
    author="centralSystem.org",
    author_email="opensource@centralSystem.org",
    description="retrieve data from centralSystem.org",
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=["central50"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'requests',
        'pandas',
        'httpx'
    ],

    python_requires='>=3'
)