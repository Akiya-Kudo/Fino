from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field, model_validator


class Target(str, Enum):
    EDINET = "edinet"


class Period(int, Enum):
    YEAR = "year"
    MONTH = "month"
    DAY = "day"


class CollectInput(BaseModel):
    target: Target
    api_key: str
    period: Period
    year: int = Field(ge=1900, le=3000, frozen=True)
    month: Optional[int] = Field(ge=1, le=12, frozen=True)
    day: Optional[int] = Field(ge=1, le=31, frozen=True)
    storage_path: str

    @model_validator(mode="after")
    def validate_period(cls, data: Any) -> Any:
        """
        期間指定の不整合をチェック
        """
        if data.period == Period.YEAR:
            if data.month is not None or data.day is not None:
                raise ValueError(
                    "month and day must not be specified when period is year"
                )
        elif data.period == Period.MONTH:
            if data.month is not str or data.day is not None:
                raise ValueError(
                    "month must be specified and day must not be specified when period is month"
                )
        elif data.period == Period.DAY:
            if data.month is None or data.day is None:
                raise ValueError(
                    "month and day must be specified when period is day"
                )
        return data


class CollectOutput(BaseModel):
    pass
