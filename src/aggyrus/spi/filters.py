from abc import ABC, abstractmethod


class BaseDigitalFilter(ABC):
    name: str

    @abstractmethod
    def apply(self, signal):
        ...

    @abstractmethod
    def design(self, *args, **kwargs):
        ...
