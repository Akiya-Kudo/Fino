"""Tests for Period model."""

from datetime import date
from typing import Literal, TypeAlias

import pytest
from fino_core.model.period import Granularity, Period


class TestPeriod:
    """Periodモデルのテスト"""

    YearArgs: TypeAlias = dict[Literal["year"], int]
    MonthArgs: TypeAlias = dict[Literal["year", "month"], int]
    DayArgs: TypeAlias = dict[Literal["year", "month", "day"], int]

    @pytest.fixture
    def period_with_year(self) -> YearArgs:
        return {
            "year": 2024,
        }

    @pytest.fixture
    def period_with_month(self) -> MonthArgs:
        return {
            "year": 2024,
            "month": 6,
        }

    @pytest.fixture
    def period_with_day(self) -> DayArgs:
        return {
            "year": 2024,
            "month": 3,
            "day": 15,
        }

    def test_create_period_with_year_only(self, period_with_year: YearArgs) -> None:
        """PeriodをYearのみで生成"""
        period = Period(**period_with_year)
        assert period.year == 2024
        assert period.month is None
        assert period.day is None
        assert period.granularity == Granularity.YEAR

        closest = period.closest_day
        assert closest == date(2024, 12, 31)

        start, end = period.to_range()
        assert start == date(2024, 1, 1)
        assert end == date(2024, 12, 31)

    def test_create_period_with_year_and_month(self, period_with_month: MonthArgs) -> None:
        """PeriodをYearとMonthで生成"""
        period = Period(**period_with_month)
        assert period.year == 2024
        assert period.month == 6
        assert period.day is None
        assert period.granularity == Granularity.MONTH

        closest = period.closest_day
        assert closest == date(2024, 6, 30)

        start, end = period.to_range()
        assert start == date(2024, 6, 1)
        assert end == date(2024, 6, 30)

    def test_create_period_with_full_date(self, period_with_day: DayArgs) -> None:
        """PeriodをYear、Month、Dayで生成"""
        period = Period(**period_with_day)
        assert period.year == 2024
        assert period.month == 3
        assert period.day == 15
        assert period.granularity == Granularity.DAY

        closest = period.closest_day
        assert closest == date(2024, 3, 15)

        start, end = period.to_range()
        assert start == date(2024, 3, 15)
        assert end == date(2024, 3, 15)

    def test_iterate_by_day_for_year(self, period_with_year: YearArgs) -> None:
        """Year: iterate_by_dayテスト"""
        period = Period(**period_with_year)
        dates = list(period.iterate_by_day())
        assert len(dates) == 366
        assert dates[0] == date(2024, 1, 1)
        assert dates[-1] == date(2024, 12, 31)

    def test_iterate_by_day_for_month(self, period_with_month: MonthArgs) -> None:
        """Month: iterate_by_dayテスト"""
        period = Period(**period_with_month)
        dates = list(period.iterate_by_day())
        assert len(dates) == 30
        assert dates[0] == date(2024, 6, 1)
        assert dates[-1] == date(2024, 6, 30)

    def test_iterate_by_day_for_day(self, period_with_day: DayArgs) -> None:
        """Day: iterate_by_dayテスト"""
        period = Period(**period_with_day)
        dates = list(period.iterate_by_day())
        assert len(dates) == 1
        assert dates[0] == date(2024, 3, 15)

    def test_closest_day_for_year(self) -> None:
        """Year: 閏年のテスト"""
        period = Period(year=2024, month=2)
        closest = period.closest_day
        # 2024年は閏年で2月の最後の日は29日
        assert closest == date(2024, 2, 29)
