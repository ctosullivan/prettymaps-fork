from setuptools import setup, find_packages

setup(
    name="prettymapsfork",
    version="0.1.0",
    author="Cormac O' Sullivan Marcelo Prates",
    author_email="cormac@cosullivan.dev marceloorp@gmail.com",
    description="A simple python library to draw pretty maps from OpenStreetMap data",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.12',
)