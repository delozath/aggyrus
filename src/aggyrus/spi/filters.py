from abc import ABC, abstractmethod

from typing import Self

import numpy as np


class BaseDigitalFilter(ABC):
    name: str

    @abstractmethod
    def apply(self, signal, *args, **kwargs) -> np.ndarray:
        ...

    @abstractmethod
    def design(self, *args, **kwargs)  -> Self | None :
        ...
