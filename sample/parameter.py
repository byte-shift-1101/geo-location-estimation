class Parameter:
    def __init__(self, key, name, unit, min_value=None, max_value=None, hooks=None):
        self.key = key
        self.name = name
        self.unit = unit
        self.min_value = min_value
        self.max_value = max_value
        self.hooks = hooks or []

    def _validate(self, value):
        if value is None:
            raise ValueError(f"Cannot set {self.key} to None.")
        if self.min_value is not None and value < self.min_value:
            raise ValueError(f"{self.key} must be greater than or equal to {self.min_value}.")
        if self.max_value is not None and value > self.max_value:
            raise ValueError(f"{self.key} must be less than or equal to {self.max_value}.")

    def __get__(self, instance, owner):
        return getattr(instance, f"_{self.key}", None)

    def __set__(self, instance, value):
        self._validate(value)
        setattr(instance, f"_{self.key}", value)
        for hook in self.hooks:
            hook(instance)

class PathParameter(Parameter):
    def __init__(self, key, name):
        super().__init__(key, name, None)

    def __get__(self, instance, owner):
        return str(super().__get__(instance, owner))