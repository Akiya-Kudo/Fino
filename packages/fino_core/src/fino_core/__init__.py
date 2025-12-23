"""Fino Core package."""

# 後方互換性のため、_modelと_factoryをエイリアス
import sys

from fino_core import factory, model

# sys.modulesに登録して、fino_core._modelとしてアクセス可能にする
sys.modules["fino_core._model"] = model
sys.modules["fino_core._factory"] = factory

__all__ = []
