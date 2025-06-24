from pydantic import BaseModel

class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    success: bool = True

    class Config:
        orm_mode = True
