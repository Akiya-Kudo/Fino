from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class EdinetDateQuery:
    start_date: date
    end_date: date


periodはapplication の概念
edinetはinfrastructure の概念でapplicationでそれらの機能とユースケースのロジックを記載し、その実態の処理はinfraに寄せる