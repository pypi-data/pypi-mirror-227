from setuptools import setup

VERSION = '1.3.0.6'
DESCRIPTION = 'For Text-based games'
LONG_DESCRIPTION = 'Oz-Engine is a Engine that allow to control characters individually like sprites you would have in a classic game engine.'

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="oz_engine",
    version=VERSION,
    author="menitoon",
    author_email="menitoine@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=["oz_engine"],
    install_requires=[],  # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'
    keywords=['python', 'text', "shell", "game"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
    ])
