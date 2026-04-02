import os
import numpy as np

from sample import constants, utils
from sample.parameter import Parameter as P, PathParameter as PP

class BaseModel:
    storage_path: PP = PP('storage_path')

    def __init__(self):
        self.SKIP_HOOKS = False
        self.UPDATE_JSON_ON_ATTRIBUTE_SET = constants.UPDATE_JSON_ON_ATTRIBUTE_SET

    def to_dict(self, materialize=False):
        overview = {key: value for key, value in vars(self.__class__).items() if isinstance(value, P) and not isinstance(value, PP)}
        if materialize:
            for key in overview.keys():
                direct = getattr(self, key) is None or isinstance(getattr(self, key), (int, float, str, list, dict, P))
                overview[key] = getattr(self, key) if direct else getattr(self, key).to_dict(materialize)
        return overview
    
    def to_str(self):
        summary = ""
        data = self.to_dict()
        
        for key, value in data.items():
            summary += f"{value.name}: "
            direct = getattr(self, key) is None or isinstance(getattr(self, key), (int, float, str, list, dict, P))
            if not direct:
                summary += "\n" + "\n".join(list(map(lambda s: f"\t{s}", getattr(self, key).to_str().split("\n"))))
            else:
                summary += f"{getattr(self, key)}"
                if value.unit is not None:
                    summary += f" {value.unit}"
            summary += "\n"
        return summary[:-1]
        
    def __str__(self):
        data = f"{self.__class__.__name__}\n"
        data += self.to_str()
        data += f"\nStored at: {self.storage_path}"
        return data