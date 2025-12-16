from datetime import date, timedelta
from enum import Enum, auto
from typing import Iterator, Optional, Tuple

from dateutil.relativedelta import relativedelta
from pydantic import BaseModel, Field, model_validator


class Granularity(Enum):
    """期間の粒度を表す列挙型"""

    YEAR = auto()
    MONTH = auto()
    DAY = auto()


class Period(BaseModel):
    """
    ### 期間を表すモデル

    指定範囲を年、月、日のいずれかで指定します。

    - year: 年単位、月単位、日単位の指定する場合に指定する。
    - month: 月単位、日単位の指定する場合に指定する。（yearが必須）
    - day: 日単位の指定する場合に指定する。（year, monthが必須）

    Pydanticによるバリデーションとシリアライゼーションを提供しつつ、
    ロジック（期間の変換、イテレーション）を内包します。
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

    @property  # @see: https://zenn.dev/yuto_mo/articles/29682f6b0c402c
    def granularity(self) -> Granularity:
        """
        Periodの粒度を取得する

        Returns
        -------
        Granularity
            期間の粒度（YEAR, MONTH, DAY）

        Examples
        --------
        >>> period = Period(year=2024, month=3, day=1)
        >>> period.granularity
        <Granularity.DAY: 3>
        """
        if self.year is not None and self.month is not None and self.day is not None:
            return Granularity.DAY
        elif self.year is not None and self.month is not None:
            return Granularity.MONTH
        elif self.year is not None:
            return Granularity.YEAR
        else:
            raise ValueError("period must be collectedly specified")

    def to_range(self) -> Tuple[date, date]:
        """
        Period を [start, end) の日付レンジに変換する

        Returns
        -------
        Tuple[date, date]
            (start, end) のタプル。endは半開区間（含まない）

        Examples
        --------
        >>> period = Period(year=2024, month=3)
        >>> start, end = period.to_range()
        >>> start
        datetime.date(2024, 3, 1)
        >>> end
        datetime.date(2024, 4, 1)
        """

        if self.granularity == Granularity.DAY:
            start = date(self.year, self.month, self.day)
            end = start + relativedelta(days=1)
        elif self.granularity == Granularity.MONTH:
            start = date(self.year, self.month, 1)
            end = start + relativedelta(months=1)
        else:
            start = date(self.year, 1, 1)
            end = start + relativedelta(years=1)

        return start, end

    def iterate_by_day(self) -> Iterator[date]:
        """
        Periodを日単位でイテレートする

        期間内のすべての日を日単位でイテレートします。
        粒度に関係なく、常に日単位で処理します。

        Yields
        ------
        date
            期間内の各日付（日単位）

        Examples
        --------
        >>> period = Period(year=2024, month=3)
        >>> dates = list(period.iterate_by_day())
        >>> dates[0]
        datetime.date(2024, 3, 1)
        >>> dates[-1]
        datetime.date(2024, 3, 31)

        >>> period = Period(year=2024)
        >>> dates = list(period.iterate_by_day())
        >>> len(dates)
        366  # 2024年はうるう年
        """
        start, end = self.to_range()
        current = start

        while current < end:
            yield current
            current += timedelta(days=1)

    def iterate(self) -> Iterator[date]:
        """
        Periodを粒度に応じて日付単位でイテレートする

        年単位の場合は年ごと、月単位の場合は月ごと、日単位の場合は日ごとに
        イテレートします。

        Yields
        ------
        date
            期間内の各日付（粒度に応じて）

        Examples
        --------
        >>> period = Period(year=2024, month=3, day=1)
        >>> list(period.iterate())
        [datetime.date(2024, 3, 1)]

        >>> period = Period(year=2024, month=3)
        >>> dates = list(period.iterate())
        >>> len(dates)
        31  # 3月は31日

        >>> period = Period(year=2024)
        >>> dates = list(period.iterate())
        >>> len(dates)
        12  # 12ヶ月
        """
        # 粒度がDAYの場合は、iterate_by_day()と同じ動作
        if self.granularity == Granularity.DAY:
            yield from self.iterate_by_day()
            return

        start, end = self.to_range()
        current = start
        g = self.granularity  # ループ外で一度だけ取得

        while current < end:
            yield current

            if g == Granularity.MONTH:
                current += relativedelta(months=1)
            else:  # Granularity.YEAR
                current += relativedelta(years=1)
