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
    
    values = materialize_dict(instance)
    # data = instance.to_dict()
    # print(f"Saving {instance.__class__.__name__} to {getattr(instance, 'storage_path')} with data: {data}")
    # for key in data.keys():
    #     direct = getattr(instance, key).__class__.__name__ == 'Parameter' or getattr(instance, key) is None
    #     print(f"Attribute {key}: {getattr(instance, key)} (Direct?: {direct})")
    #     if not direct:
    #         print(f"Nested data for {key}: {getattr(instance, key).to_dict()}")
    # values = {key: (getattr(instance, key) if (getattr(instance, key) is None or getattr(instance, key).__class__.__name__ == 'Parameter') else getattr(instance, key).to_dict()) for key in data.keys()}
    # print(f"Values to save: {values}")
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

def materialize_dict(instance):
    filled = {}
    data = instance.to_dict()
    for key in data.keys():
        trivial_value = getattr(instance, key) is None or getattr(instance, key).__class__.__name__ == 'Parameter' or isinstance(getattr(instance, key), (int, float, str, list, dict))
        filled[key] = getattr(instance, key) if trivial_value else materialize_dict(getattr(instance, key))
    return filled

def to_str(instance):
    summary = ""
    data = instance.to_dict()
    for key, value in data.items():
        if (not getattr(instance, key) is None and getattr(instance, key).__class__.__name__ != 'Parameter' and not isinstance(getattr(instance, key), float) and not isinstance(getattr(instance, key), int) and not isinstance(getattr(instance, key), str) and not isinstance(getattr(instance, key), list) and not isinstance(getattr(instance, key), dict)):
            details = to_str(getattr(instance, key)).split("\n")
            summary += "\n".join(list(map(lambda x: f"\t{x}", details)))
        else:
            summary += f"\t{value.name}: {getattr(instance, key)}"
            if value.unit is not None:
                summary += f" {value.unit}"
            summary += "\n"

    return f"{instance.__class__.__name__}\n{summary}"