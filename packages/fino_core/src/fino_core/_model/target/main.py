from enum import Enum
from typing import Union

from .edinet.main import EdinetTargetConfig, EdinetTargetPort


class TargetType(str, Enum):
    EDINET = "edinet"


TargetPort = Union[EdinetTargetPort]

TargetConfig = Union[EdinetTargetConfig]
