from pathlib import Path
import json

def get_config(file_name):
    """
    Reads file and returns deserialized json
    :params str file_name: file path of config file
    :returns json 
    """
    p = Path(file_name)
    if p.exists():
        with p.open() as f:
            return json.loads(f.read())
    return False
