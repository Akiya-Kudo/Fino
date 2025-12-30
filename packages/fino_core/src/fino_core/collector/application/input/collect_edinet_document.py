from dataclasses import dataclass

from fino_core.collector.application.port.storage import Storage
from fino_core.util.timescope import TimeScope


@dataclass
class CollectEdinetDocumentInput:
    timescope: TimeScope
    storage: Storage
    edinet: Edinet
