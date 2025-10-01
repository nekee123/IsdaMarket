from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    uid: str
    email: EmailStr
    user_type: str  # "buyer" or "seller"
