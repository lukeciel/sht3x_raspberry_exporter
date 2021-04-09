import re
from setuptools import setup

requires = [
    "pyramid",
    "smbus",
    "waitress",
    "pytest",
]

version = ""
with open("sht3x_raspberry_exporter/__init__.py") as fp:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fp.read(), re.MULTILINE).group(1)

readme = ""
with open("README.md") as fp:
    readme = fp.read()

setup(
    name="sht3x_raspberry_exporter",
    version=version,
    description="A Prometheus exporter for the SHT3x humidity and temperature sensor.",
    long_description=readme,
    author="lukeciel",
    author_email="lukas@lukes.space",
    url="https://github.com/lukeciel/sht3x_exporter_raspberry",
    licence="MIT",
    install_requires=requires,
    entry_points={
        "paste.app_factory": [
            "main = sht3x_raspberry_exporter:main"
        ]
    }
)