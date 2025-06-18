from setuptools import setup, find_packages

setup(
    name="Blackout",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["scapy"],
    entry_points={
        "console_scripts": [
            "blackout=blackout.cli:main",
        ],
    },
    description="Raw packet network flooder",
    author="0xf0xy",
    license="MIT",
)
