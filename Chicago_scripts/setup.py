from setuptools import find_packages, setup

with open("./README.rst") as f:
    long_description = f.read()

requirements = []

setup(
    name="rcv",
    version="0.1.2",
    description="Tabulate ballots from ranked-choice elections",
    author="Max Hully",
    author_email="max@mggg.org",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/gerrymandr/rcv",
    packages=find_packages(exclude=("tests",)),
    install_requires=requirements,
    extras_require={
        "test": ["pandas", "pytest", "pytest-cov"],
        "sample": ["numpy >= 1.7"],
    },
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: BSD License",
    ],
)
