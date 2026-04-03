import os
import numpy as np
import json
from typing import get_args, get_origin, get_type_hints

from sample import constants, hooks, utils
from sample.parameter import Parameter as P, PathParameter as PP

class BaseModel:
    name : P[str] = P('name', None)
    storage_path: PP = PP('storage_path')

    def __init__(self, name=None):
        self.SKIP_HOOKS = False
        self.UPDATE_JSON_ON_ATTRIBUTE_SET = constants.UPDATE_JSON_ON_ATTRIBUTE_SET

        self.fill_initial_values(name)

    @hooks.disable_other_hooks
    def fill_initial_values(self, name):
        class_name = utils.unformalize_str(self.__class__.__name__)
        storage_filename = os.path.join(class_name, f"{name}.json") if name is not None else f"{class_name}.json"

        self.storage_path = utils.get_unique_path(os.path.join(constants.CONFIG_FOLDER, storage_filename))
        if name is not None:
            self.name = name

    @hooks.disable_other_hooks
    def set_initial(self, key, value):
        setattr(self, key, value)

    def save(self):
        os.makedirs(os.path.dirname(getattr(self, 'storage_path')), exist_ok=True)
        values = self._jsonify_value(self.to_dict(materialize=True))
        with open(getattr(self, 'storage_path'), 'w') as f:
            json.dump(values, f, indent=4)

    def load(self):
        with open(getattr(self, 'storage_path'), 'r') as f:
            data = json.load(f)

        fields = list(self.to_dict().keys())
        setattr(self, 'SKIP_HOOKS', True)
        for key, value in data.items():
            if not hasattr(self, key):
                raise ValueError(f"Cannot load data. {self.__class__.__name__} has no attribute '{key}'.")

            setattr(self, key, utils.coerce_value(self, key, value))
            if key in fields:
                fields.remove(key)

        for field in fields:
            setattr(self, field, None)
        setattr(self, 'SKIP_HOOKS', False)

    def _jsonify_value(self, value):
        if isinstance(value, np.ndarray):
            return value.tolist()
        if isinstance(value, dict):
            return {key: self._jsonify_value(inner_value) for key, inner_value in value.items()}
        if isinstance(value, list):
            return [self._jsonify_value(item) for item in value]
        return value

    def _parameter_descriptors(self):
        descriptors = {}
        for cls in self.__class__.mro()[::-1]:
            for key, value in vars(cls).items():
                if isinstance(value, P) and not isinstance(value, PP):
                    descriptors[key] = value
        return descriptors

    def to_dict(self, materialize=False):
        overview = self._parameter_descriptors()
        if materialize:
            for key in overview.keys():
                direct = getattr(self, key) is None or isinstance(getattr(self, key), (int, float, str, list, dict, np.ndarray, P))
                overview[key] = getattr(self, key) if direct else getattr(self, key).to_dict(materialize)
        return overview
    
    def to_str(self):
        summary = ""
        data = self.to_dict()
        
        for key, value in data.items():
            summary += f"{value.name}: "
            is_complex = isinstance(getattr(self, key), BaseModel)
            if is_complex:
                summary += "\n" + "\n".join(list(map(lambda s: f"\t{s}", getattr(self, key).to_str().split("\n"))))
            else:
                summary += f"{getattr(self, key)}"
                if value.unit is not None:
                    summary += f" {value.unit}"
            summary += "\n"
        return summary[:-1]
        
    def __str__(self):
        data = f"{self.__class__.__name__}\n"
        data += "\n".join(list(map(lambda s: f"\t{s}", self.to_str().split("\n"))))
        data += f"\nStored at: {self.storage_path}"
        return data