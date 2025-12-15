from typing import List

from pydantic import BaseModel

from fino_core._model.period import Period
from fino_core._model.storage import Storage
from fino_core._model.target.main import TargetType


class CollectInput(BaseModel):
    target: TargetType
    api_key: str
    period: Period
    storage: Storage


class CollectOutput(BaseModel):
    documents: List[str]
