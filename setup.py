from setuptools import find_packages,setup
from typing import List

def get_requirements(file_path:str)->List[str]:
    '''
    this function will return the list of requirements
    '''
    requirements=[]
    with open(file_path) as file_obj:
        requirements=file_obj.readlines()
        requirements=[req.replace("\n","") for req in requirements]
        requirements = requirements.remove('-e .')
    
    return requirements

setup( name      = 'Assignment', version = '0.0.1', author ='Vahid Derakhshan',
author_email     = 'vahid.derakhshan@gmail.com',
packages         = find_packages(),
install_requires = get_requirements('requirements.txt')

)