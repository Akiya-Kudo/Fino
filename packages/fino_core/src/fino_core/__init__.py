"""Fino Core package."""

from fino_core.api.collect_edinet import (
    CollectDocumentInput,
    PeriodInput,
    StorageConfigInput,
    collect_edinet,
)
from fino_core.domain.storage_type import StorageType

__all__ = [
    # Public API
    "collect_edinet",
    "CollectDocumentInput",
    "PeriodInput",
    "StorageConfigInput",
    "StorageType",
]
