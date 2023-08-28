from setuptools import setup

setup(
    name="cogo",
    version="0.0.1",
    install_requires=[
        "argparse",
        "toml",
    ],
    entry_points={
        "console_scripts": [
            "cogo = main:main",
        ],
    },
)
