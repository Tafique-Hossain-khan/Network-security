from src.logging import logger
from src.exception.exception import CustomeException
from dataclasses import dataclass
import os,sys
import pandas as pd
import yaml

def read_yaml(yaml_file_path):
    try:
        with open(yaml_file_path, 'r') as file:
            yaml_content = yaml.safe_load(file)

        return yaml_content
    except Exception as e:
        raise CustomeException(e,sys)
    

def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, "w") as file:
            yaml.dump(content, file)
        
    except Exception as e:
        raise CustomeException(e, sys)
