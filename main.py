from fastapi import FastAPI
from db import init_db
from config import get_settings
from schemas.user import BaseUser
from schemas.base import BaseResponse
from models.user import User

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="FastAPI CRUD Tortoise-orm with aerich",
    debug=settings.app_debug,
)


@app.on_event("startup")
async def startup():
    await init_db()
    print("DB Connected ✅")

@app.on_event("shutdown")
async def shutdown():
    await init_db()
    print("DB DisConnected ❌")


@app.get("/users", response_model=BaseResponse)
async def get_users():
    users = await User.all()
    data = users
    return BaseResponse(data=data)

@app.post("/user", response_model=BaseResponse)
async def create_user(user: BaseUser):
    user_data = await User.create(
        email=user.email,
        username=user.username,
        password=user.password
    )

    data = {
        "email": user_data.email,
        "username": user_data.username,
        "password": user_data.password
    }
    return BaseResponse(data=data)

