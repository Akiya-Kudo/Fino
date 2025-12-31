from dataclasses import dataclass

from fino_core.domain.model import ValueObject


@dataclass(frozen=True, slots=True)
class DisclosureSource(ValueObject):
    name: str

    def _validate(self) -> None:
        if not self.name:
            raise ValueError("Disclosure source cannot be empty")
