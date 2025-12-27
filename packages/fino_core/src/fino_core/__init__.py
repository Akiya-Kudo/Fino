"""Fino Core package."""

from fino_core import domain, factory
from fino_core.api.collect_edinet import (
    CollectDocumentInput,
    PeriodInput,
    StorageConfigInput,
    collect_edinet,
)
from fino_core.domain.storage_type import StorageType

__all__ = [
    # Internal modules
    "domain",
    "factory",
    # Public API
    "collect_edinet",
    "CollectDocumentInput",
    "PeriodInput",
    "StorageConfigInput",
    "StorageType",
]
