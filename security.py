from passlib.context import CryptContext
from jose import jwt
from datetime import datetime,timedelta

context = CryptContext(schemes=["bcrypt"] , deprecated="auto")
SECRET_KEY = "rohitsinghrajput" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRES_MINUTES = 30

def hashpass(password : str):
    return context.hash(password)


def verifypass(password : str , hashed : str):
    return context.verify(password , hashed)


def create_access_token(data : dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
    to_encode.update({"exp" : expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    


