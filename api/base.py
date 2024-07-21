from fastapi import APIRouter

from schema.base import ResponseBase, ErrorResponse
from const import code

api = APIRouter(tags=["api"])


@api.get("/", response_model=ResponseBase | ErrorResponse)
async def get_root():
    return ResponseBase(code=code.OK)
