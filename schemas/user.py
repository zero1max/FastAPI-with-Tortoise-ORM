from pydantic import BaseModel, EmailStr

class BaseUser(BaseModel):
    email: EmailStr
    username: str
    password: str

    class Config:
        orm_mode = True


class UserOut(BaseModel):
    id: int
    email: str
    username: str

    class Config:
        from_attributes = True 