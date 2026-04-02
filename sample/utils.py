import os
from collections.abc import Iterable

def get_unique_path(standard_path):
    if not os.path.exists(standard_path):
        return standard_path

    base, ext = os.path.splitext(standard_path)
    counter = 1
    new_path = f"{base}_{counter}{ext}"
    while os.path.exists(new_path):
        counter += 1
        new_path = f"{base}_{counter}{ext}"
    return new_path

def params_exist(instance, params):
    for param in params:
        if getattr(instance, param) is None:
            return False
    return True

def is_array(instance):
    return isinstance(instance, Iterable) and not isinstance(instance, (str, bytes))

def formalize_str(s):
    return s.strip().replace("_", " ").title()

def unformalize_str(s):
    return s.strip().replace(" ", "_").lower()