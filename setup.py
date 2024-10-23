
from setuptools import setup,find_packages

def get_requirements()->list:
    """ 
    This fucntion will read all the requirements for the requirements.txt file

    return:
    It will return a list that contain all the dependencies
    """

    try:
        requirements_list = []
        with open("requirements.txt",'r') as f:
            requirements = f.readlines()
            for lib in requirements:
                req = lib.strip()
                if req and req != "-e .":
                    requirements_list.append(req)

        return requirements_list
            
    except FileExistsError:
        print("File does not exist")


setup(
    setup(
    name="NetworkSecurity",
    version="0.0.1",
    author="Tafique Hossain Khan",
    author_email="tafiquehossain2003@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements()
)
)