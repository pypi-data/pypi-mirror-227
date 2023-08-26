from setuptools import setup

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="iroh",
    description="Bytes. Distributed.",
    long_description=long_description,
    version="0.0.4",
    author="n0 team",
    url="https://github.com/n0-computer/iroh",
    license="MIT OR Apache-2.0",
    install_requires=["setuptools"],
)
