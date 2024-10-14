from setuptools import find_packages, setup
from typing import List

def get_requirements(file_path: str) -> List[str]:
    '''
    Reads a requirements file and returns a list of dependencies.

    Args:
        file_path (str): The path to the requirements file.

    Returns:
        List[str]: A list of package requirements.

    This function reads the specified requirements file line by line, 
    removes newline characters, and filters out any editable install ('-e .') entry.
    '''
    requirements = []
    # Open the specified requirements file
    with open(file_path) as file_obj:
        # Read all lines and strip out newline characters
        requirements = file_obj.readlines()
        requirements = [req.replace("\n", "") for req in requirements]
        # Remove the '-e .' entry if it exists (used for editable installs)
        requirements = requirements.remove('-e .') if '-e .' in requirements else requirements
    
    return requirements

# Setup configuration for the package
setup(
    name='Assignment',                      # Name of the package
    version='0.0.1',                        # Initial version of the package
    author='Vahid Derakhshan',              # Author's name
    author_email='vahid.derakhshan@gmail.com', # Author's email
    packages=find_packages(),               # Automatically find and include all packages
    install_requires=get_requirements('requirements.txt') # Install dependencies listed in requirements.txt
)
