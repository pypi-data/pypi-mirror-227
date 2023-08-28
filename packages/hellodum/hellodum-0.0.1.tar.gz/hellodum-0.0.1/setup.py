from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'A Simple Hello package, bro!'
LONG_DESCRIPTION = "Hasnain ne task diys tha kr liya"

setup(
    name='hellodum',
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    author='Huzaifa',
    author_email='huzaifat65@outlook.com',
    install_requires=['numpy'],
    classifiers=[
        # "Development State :: Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        ""
    ]
)