import yaml
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import os, sys
import numpy as np
import pickle

def read_yaml(file_path:str) -> dict:
    try:
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)


def write_yaml(filepath : str , content : object , replace:bool = False )->None:
    try:
        if replace:
            if os.path.exists(filepath):
                os.remove(filepath)
        
        os.makedirs(os.path.dirname(filepath),exist_ok=True)
        with open(filepath,'w') as file :
            yaml.dump(content,file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)