from typing import Dict
from xmlrpc.client import Boolean

pids = []
remember_dict: Dict[str, object] = {
    "packages": [],
    "pid": ""
}


def chek_gloable_value_equal(key, value) -> Boolean:
    if key in remember_dict:
        if remember_dict[key] == value:
            return True
    remember_dict[key] = value
    return False
