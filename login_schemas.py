from pydantic import BaseModel
from typing import Optional


class LoginRegisterSchema(BaseModel):
    id: Optional[str]
    user_name: str
    password: str
