from pydantic import BaseModel


class ResponseBase(BaseModel):
    code: int


class ErrorResponse(ResponseBase):
    detail: str
