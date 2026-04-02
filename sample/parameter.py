from __future__ import annotations
from typing import overload, TypeVar, Generic
from sample import hooks, utils

T = TypeVar('T')

class Parameter(Generic[T]):
    def __init__(
            self, key: str, unit: str | None, name: str | None = None, can_be_none: bool = False,
            min_value: int | float | None = None, max_value: int | float | None = None, strict_length: int | None = None,
            hooks=[hooks.hook_auto_save]
        ):
        self.key = key
        self.name = name or utils.formalize_str(key)
        self.unit = unit
        self.can_be_none = can_be_none
        self.min_value = min_value
        self.max_value = max_value
        self.strict_length = strict_length
        self.hooks = hooks or []

    def _validate(self, value):
        if value is None:
            if not self.can_be_none:
                raise ValueError(f"Cannot set {self.key} to None.")
            return
        if self.strict_length is not None:
            if not utils.is_array(value):
                raise ValueError(f"{self.key} must be an array with exactly {self.strict_length} elements.")
            if len(value) != self.strict_length:
                raise ValueError(f"{self.key} must be an array with exactly {self.strict_length} elements.")
        if self.min_value is not None:
            if utils.is_array(value):
                for v in value:
                    if v < self.min_value:
                        raise ValueError(f"{self.key} must be greater than or equal to {self.min_value}.")
            elif value < self.min_value:
                raise ValueError(f"{self.key} must be greater than or equal to {self.min_value}.")
        if self.max_value is not None:
            if utils.is_array(value):
                for v in value:
                    if v > self.max_value:
                        raise ValueError(f"{self.key} must be less than or equal to {self.max_value}.")
            elif value > self.max_value:
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

class PathParameter(Parameter[str]):
    def __init__(self, key, name=None):
        super().__init__(key, None, name=name, hooks=[])