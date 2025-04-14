from fastapi import FastAPI, HTTPException
from db import init_db
from config import get_settings
from schemas.user import BaseUser, UserOut
from schemas.base import BaseResponse
from models.user import User
from tortoise import Tortoise
from tortoise.exceptions import IntegrityError


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="FastAPI CRUD Tortoise-orm with aerich",
    debug=settings.app_debug,
)

# ----------------------------------------------------

@app.on_event("startup")
async def startup():
    await init_db()
    print("DB Connected ✅")

@app.on_event("shutdown")
async def shutdown():
    await Tortoise.close_connections()
    print("DB Disconnected ❌")

# ----------------------------------------------------

@app.get("/users", response_model=BaseResponse)
async def get_users():
    users = await User.all()
    user_list = [UserOut.model_validate(user) for user in users]
    return BaseResponse(status=True, data=user_list)


@app.post("/user", response_model=BaseResponse)
async def create_user(user: BaseUser):
    try:
        user_data = await User.create(
            email=user.email,
            username=user.username,
            password=user.password  
        )

        data = {
            "email": user_data.email,
            "username": user_data.username,
        }
        return BaseResponse(status=True, data=data)
    except IntegrityError as e:
        error_msg = str(e)
        if "email" in error_msg.lower():
            raise HTTPException(status_code=400, detail="Email already exists")
        elif "username" in error_msg.lower():
            raise HTTPException(status_code=400, detail="Username already exists")
        else:
            raise HTTPException(status_code=400, detail=str(e))

@app.put("/users/{user_id}", response_model=BaseResponse)
async def update_user(user_id: int, user_data: BaseUser):
    user = await User.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        user.username = user_data.username
        user.email = user_data.email
        await user.save()

        return BaseResponse(status=True, data=UserOut.model_validate(user))
    except IntegrityError as e:
        error_msg = str(e)
        if "email" in error_msg.lower():
            raise HTTPException(status_code=400, detail="Email already exists")
        elif "username" in error_msg.lower():
            raise HTTPException(status_code=400, detail="Username already exists")
        else:
            raise HTTPException(status_code=400, detail=str(e))

@app.delete("/users/{user_id}", response_model=BaseResponse)
async def delete_user(user_id: int):
    user = await User.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await user.delete()
    return BaseResponse(status=True, data=f"User {user_id} deleted")
