from abc import ABC, abstractmethod


import numpy as np


class BaseDigitalFilter(ABC):
    name: str

    @abstractmethod
    def apply(self, signal, *args, **kwargs) -> np.ndarray:
        ...

    @abstractmethod
    def design(self, *args, **kwargs):
        ...
