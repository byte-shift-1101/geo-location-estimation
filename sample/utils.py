import os
import numpy as np
from typing import get_type_hints, get_args, get_origin
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

def coerce_value(instance, key, value):
    if value is None:
        return None

    type_hints = get_type_hints(instance.__class__)
    annotation = type_hints.get(key)
    if annotation is None:
        return value

    parameter_args = get_args(annotation)
    if len(parameter_args) == 0:
        return value

    expected_type = parameter_args[0]
    if is_numpy_array_annotation(expected_type) and is_array(value):
        return np.asarray(value)

    return value

def is_array(instance):
    return isinstance(instance, Iterable) and not isinstance(instance, (str, bytes))

def is_numpy_array_annotation(expected_type):
    origin = get_origin(expected_type)
    if origin is np.ndarray:
        return True
    if expected_type is np.ndarray:
        return True
    return 'ndarray' in str(expected_type).lower()

def formalize_str(s):
    return s.strip().replace("_", " ").title()

def unformalize_str(s):
    return s.strip().replace(" ", "_").lower()