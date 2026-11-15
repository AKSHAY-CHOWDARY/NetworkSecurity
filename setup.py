from setuptools import find_packages, setup
from typing import List

def get_requirements(file_path) -> List[str]:
    """
        This function will return list of requirements
    """
    requirements:List[str] = []

    try:
        with open(file_path,'r') as file:
            ## Read lines from file
            lines = file.readlines()
            ### Process each line
            for line in lines:
                requirement = line.strip()
                ### Ignore empty lines and ignore -e.
                if requirement and requirement != '-e .':
                    requirements.append(requirement)
    except FileNotFoundError:
        print(f"{file_path} file not found.")

    return requirements


setup(
    name='NetworkSecurity',
    version="0.0.1",
    author="Akshay",
    author_email="k.v.akshay111@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements("requirements.txt")
)
