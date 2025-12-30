"""Fino Core package."""

# Public API exports
# 後方互換性のため、_modelと_factoryをエイリアス
import sys

from fino_core import domain, factory
from fino_core.api.collect_edinet import (
    CollectDocumentInput,
    PeriodInput,
    StorageConfigInput,
    collect_edinet,
)
from fino_core.domain.storage_type import StorageType

# sys.modulesに登録して、fino_core._modelとしてアクセス可能にする（後方互換性）
sys.modules["fino_core._model"] = domain
sys.modules["fino_core._factory"] = factory
sys.modules["fino_core.model"] = domain  # 後方互換性のため

__all__ = [
    "collect_edinet",
    "CollectDocumentInput",
    "PeriodInput",
    "StorageConfigInput",
    "StorageType",
]
