from abc import ABC, abstractmethod
from typing import override

@abstractmethod
class BaseDescriptor:
    def __set_name__(self, owner, name):
        self.name = name
        self.private_name = '_' + name
    
    def __get__(self, obj, objtype=None):
        if obj is None: 
            return self
        if hasattr(obj, self.private_name):
            return getattr(obj, self.private_name)
        else:
            raise ValueError(f"Attribute {self.name} have not being set")
    
    def __set__(self, obj, value):
        self._validate(obj, value)
        setattr(obj, self.private_name, value)
    
    @abstractmethod
    def _validate(self, obj, value):
        """
        Raises exeptions if the value does not comply with the descriptor rules
        """
        ...


class MutableDescr(BaseDescriptor):
    def __set__(self, obj, value):
        setattr(obj, self.private_name, value)


class NonMutableDescr(BaseDescriptor):
    @override
    def _validate(self, obj, value):
        if hasattr(obj, self.private_name):
            raise ValueError(f"{self.name} can only be assigned once")
 

class TypedNonMutableDescr(BaseDescriptor):
    def __init__(self, expected_type) -> None:
        self._TYPE = expected_type
    
    @override
    def _validate(self, obj, value):
        if hasattr(obj, self.private_name):
            raise ValueError(f"{self.name} can only be assigned once")
        if not isinstance(value, self._TYPE):
            raise TypeError(
                    f"Expected type for the attribute `{self.name}` is `{self._TYPE.__name__}`,"
                    f"but `{type(value).__name__}` was provided instead"
                )


class TypedMutableDescr(BaseDescriptor):
    def __init__(self, expected_type) -> None:
        self._TYPE = expected_type
    
    @override
    def _validate(self, obj, value):
        if not isinstance(value, self._TYPE):
            raise TypeError(
                    f"Expected type for the attribute `{self.name}` is `{self._TYPE.__name__}`,"
                    f"but `{type(value).__name__}` was provided instead"
                )
