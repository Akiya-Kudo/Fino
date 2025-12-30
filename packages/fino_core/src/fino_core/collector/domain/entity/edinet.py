
from dataclasses import dataclass

from .entity import Entity


@dataclass
class Edinet(Entity):
    def get_document_list(): 