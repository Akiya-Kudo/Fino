from dataclasses import dataclass

from fino_core.util.timescope import TimeScope


@dataclass
class CollectorCollectDocumentInputDTO:
    timescope: TimeScope
