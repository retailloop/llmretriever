from abc import ABC, abstractmethod
from typing import Any


class CachePort(ABC):
    @abstractmethod
    def get(self, key: str) -> Any:
        pass

    @abstractmethod
    def set(self, key: str, value: Any, expiration: int = 3600):
        pass
