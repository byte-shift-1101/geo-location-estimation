import os
import json
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

def save(instance):
    if instance is None:
        raise ValueError("Cannot save data from None instance.")
    
    data = instance.to_dict()
    values = {key: getattr(instance, key) for key in data.keys()}
    with open(getattr(instance, 'storage_path'), 'w') as f:
        json.dump(values, f, indent=4)

def load(instance):
    if instance is None:
        raise ValueError("Cannot load data into None instance.")
    
    with open(getattr(instance, 'storage_path'), 'r') as f:
        data = json.load(f)

    fields = list(instance.to_dict().keys())

    setattr(instance, 'SKIP_HOOKS', True)
    for key, value in data.items():
        if not hasattr(instance, key):
            raise ValueError(f"Cannot load data. {instance.__class__.__name__} has no attribute '{key}'.")

        setattr(instance, key, value)
        fields.remove(key)

    for field in fields:
        setattr(instance, field, None)
    setattr(instance, 'SKIP_HOOKS', False)

def to_str(instance):
    data = instance.to_dict()
    summary = ""
    for key, value in data.items():
        summary += f"\t{value.name}: {getattr(instance, key)}"
        if value.unit is not None:
            summary += f" {value.unit}"
        summary += "\n"

    return f"{instance.__class__.__name__}\n{summary}"