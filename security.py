import bcrypt
from jose import jwt
from datetime import datetime,timedelta
from fastapi import Depends, HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

SECRET_KEY = "rohitsinghrajput" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRES_MINUTES = 30

def hashpass(password : str):
  
    if not isinstance(password, str):
        password = str(password)
   
    password_bytes = password.encode('utf-8')
   
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
  
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
 
    return hashed.decode('utf-8')


def verifypass(password : str , hashed : str):

    if not isinstance(password,str):
        password = str(password)
    
    password_bytes = password.encode('utf-8')

    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]

        
    hashed_bytes = hashed.encode('utf-8')

    return bcrypt.checkpw(password_bytes, hashed_bytes)




def create_access_token(data : dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
    to_encode.update({"exp" : expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    


oauth_schema = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token : str = Depends(oauth_schema)):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        email = payload.get("email")
        if email is None:
            raise HTTPException(status_code=404, detail="Invalid token buddy")
        return email
    except JWTError:
        raise HTTPException(status_code=404, detail="internal server error")    


