from typing import Optional

from pydantic import BaseModel, Field, model_validator


class Period(BaseModel):
    """
    ### 期間の指定。指定範囲を年、月、日のいずれかで指定する。

    - year: 年単位、月単位、日単位の指定する場合に指定する。
    - month: 月単位、日単位の指定する場合に指定する。（yearが必須）
    - day: 日単位の指定する場合に指定する。（year, monthが必須）

    ※ ドメインとしての意味はないため、Pydanticによるバリデーションyテックを含めたModalとする
    """

    year: int = Field(ge=1900, le=3000, frozen=True)
    month: Optional[int] = Field(ge=1, le=12, frozen=True)
    day: Optional[int] = Field(ge=1, le=31, frozen=True)

    @model_validator(mode="after")
    def validate_period(cls, data: "Period") -> "Period":
        """
        期間指定の不整合をチェック
        """
        if data.day is not None and data.month is None:
            raise ValueError("month must be specified when day is specified")
        return data
