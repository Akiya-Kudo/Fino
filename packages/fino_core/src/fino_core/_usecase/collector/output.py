from pydantic import BaseModel


class CollectOutput(BaseModel):
    documents: list[str]
