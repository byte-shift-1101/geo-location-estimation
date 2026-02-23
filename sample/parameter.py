from __future__ import annotations
from typing import overload, TypeVar, Generic
from sample import hooks

T = TypeVar('T')

class Parameter(Generic[T]):
    def __init__(self, key, unit, name=None, min_value=None, max_value=None, hooks=[hooks.hook_auto_save]):
        self.key = key
        self.name = name or self.__derive_name(key)
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

    @overload
    def __get__(self, instance: None, owner: type) -> Parameter[T]: ...
    @overload
    def __get__(self, instance: object, owner: type) -> T: ...
    def __get__(self, instance, owner):
        return getattr(instance, f"_{self.key}", None)

    def __set__(self, instance, value):
        self._validate(value)
        setattr(instance, f"_{self.key}", value)

        if getattr(instance, 'SKIP_HOOKS', False):
            return
        for hook in self.hooks:
            hook(instance)

    def __derive_name(self, key):
        name = key.replace('_', ' ').title()
        return name

class PathParameter(Parameter[str]):
    def __init__(self, key, name=None):
        super().__init__(key, None, name=name, hooks=[])