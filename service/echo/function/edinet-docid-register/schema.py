from aws_lambda_powertools.utilities.parser import BaseModel


# TypedDict型定義（型チェッカー用）
class EventDetail(BaseModel):
    document_ids: list[str]
    sec_code: str


class InputEvent(BaseModel):
    detail: EventDetail
    detailType: str


class OutputBody(BaseModel):
    sec_code: str
    saved_count: int


class OutputEvent(BaseModel):
    statusCode: int
    body: OutputBody
