from setuptools import setup, find_packages

setup(
    name="aifix",
    version="0.2",
    packages=find_packages(),
    install_requires=[
        "openai",
    ],
    entry_points={
        "console_scripts": [
            "aifix = aifix.cli:main",
        ],
    },
)
