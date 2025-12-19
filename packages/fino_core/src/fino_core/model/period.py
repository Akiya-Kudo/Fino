from datetime import date, timedelta
from enum import Enum, auto
from typing import Any, Iterator, Self, Tuple

from dateutil.relativedelta import relativedelta
from pydantic import BaseModel


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

    year: int
    month: int | None = None
    day: int | None = None

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
        # yearは必須（int型）なので、monthとdayのみをチェック
        if self.month is not None and self.day is not None:
            return Granularity.DAY
        elif self.month is not None:
            return Granularity.MONTH
        else:
            # yearのみが指定されている場合
            return Granularity.YEAR

    @property
    def closest_day(self) -> date:
        """
        Periodの最も近い日を取得する
        """
        if self.granularity == Granularity.DAY:
            return date(self.year, self.month or 1, self.day or 1)
        elif self.granularity == Granularity.MONTH:
            return date(self.year, self.month or 1, 1) + relativedelta(months=1) - timedelta(days=1)
        else:
            return date(self.year, 1, 1) + relativedelta(years=1) - timedelta(days=1)

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
        datetime.date(2024, 3, 31)
        """

        if self.granularity == Granularity.DAY:
            start = date(self.year, self.month, self.day)
            end = start
        elif self.granularity == Granularity.MONTH:
            start = date(self.year, self.month, 1)
            end = start + relativedelta(months=1) - timedelta(days=1)
        else:
            start = date(self.year, 1, 1)
            end = start + relativedelta(years=1) - timedelta(days=1)

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

    @classmethod
    def from_input(cls, input: Any) -> Self:
        return cls(
            year=input.year,
            month=input.month,
            day=input.day,
        )
