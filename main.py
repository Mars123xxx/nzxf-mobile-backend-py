import uvicorn
from fastapi import FastAPI

from api.base import api
from api.user.user import api_user
from const import code
from db import models
from db.database import engine
from middleware.auth import AuthMiddleware
from schema.base import ResponseBase, ErrorResponse

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# 将子应用添加到主应用
app.include_router(api, prefix="/api")  # 添加前缀 '/api
app.include_router(api_user, prefix="/api/user")  # 添加前缀 '/api
# app.add_middleware(AuthMiddleware)

@app.get("/", response_model=ResponseBase | ErrorResponse,tags=[""])
async def get_root():
    return ResponseBase(code=code.OK)


if __name__ == "__main__":
    uvicorn.run("main:app", port=8889)
