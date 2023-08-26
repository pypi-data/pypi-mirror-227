from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Self, Set


class ParseChoicesType(Enum):
    SET = 0
    LIST = 1


class SettingsEnumBase(ABC):
    parse_choices_type: ParseChoicesType = ParseChoicesType.SET

    @classmethod
    def choices(cls) -> List[str]:
        return sorted(item.item_to_choice() for item in cls)

    @classmethod
    def all(cls) -> Set[Self]:
        return {item for item in cls}

    @classmethod
    def parse_choices(cls, choices: str) -> List[Self]:
        container = set if cls.parse_choices_type == ParseChoicesType.SET else list
        return container(cls.parse_choice(choice) for choice in choices)

    @classmethod
    def parse_choice(cls, choice: str) -> Self:
        return choice.replace("-", "_").upper()

    def item_to_choice(self) -> str:
        return self.name.replace("_", "-").lower()

    def __str__(self):
        return self.item_to_choice()

    @abstractmethod
    def __iter__(self):
        ...

    @abstractmethod
    def name(self) -> str:
        ...

    @abstractmethod
    def value(self) -> str:
        ...
