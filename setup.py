from setuptools import find_packages,setup
from typing import List

REQUIREMENTS_FILENAME = 'requirements.txt'

def get_requirements()->List[str]:
    with open(REQUIREMENTS_FILENAME) as f:
        requirements_list = [filenames.replace('\n',"") for filenames in f.readlines()]




setup(
    name = 'sensor',
    version = "1.0",
    author = "sanjay",
    author_emial = "sanjaysanjay1270@gmail.com",
    pakages = find_packages(),
    install_requires = get_requirements(),
)