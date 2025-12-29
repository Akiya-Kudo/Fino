from dataclasses import dataclass
from enum import Enum


class DataSource(Enum):
    """データソースの種類"""

    EDINET = "edinet"
    TDNET = "tdnet"


@dataclass(frozen=True)
class Source:
    """データソースを表現するValue Object

    許可されたデータソースのみを受け付けます。
    """

    value: str

    def __post_init__(self) -> None:
        """ドメイン不変条件の検証"""
        if not self.value or not self.value.strip():
            raise ValueError("Source must not be empty")
        source = self.value.strip().upper()
        try:
            _ = DataSource(source)
        except ValueError as err:
            raise ValueError(
                f"Source must be one of {[ds.value for ds in DataSource]}: {source}"
            ) from err

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return f"Source('{self.value}')"

    @property
    def is_edinet(self) -> bool:
        """EDINETソースかどうかを判定"""
        return self.value.strip().lower() == DataSource.EDINET.value

    @property
    def is_tdnet(self) -> bool:
        """TDNETソースかどうかを判定"""
        return self.value.strip().lower() == DataSource.TDNET.value
