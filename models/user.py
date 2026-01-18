from pydantic import BaseModel, EmailStr

class users(BaseModel):
    username : str
    email : EmailStr
    password : str