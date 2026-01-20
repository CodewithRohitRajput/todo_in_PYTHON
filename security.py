import bcrypt
from jose import jwt
from datetime import datetime,timedelta
from fastapi import Depends, HTTPException, Request
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
    




async def get_current_user(request : Request):
   try:
       token = request.cookies.get("access_token") or (
       request.headers.get("Authorization", "").removeprefix("Bearer ").strip() or None
       )

       if not token:
              raise HTTPException(status_code=404,detail="token not found")

       payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
       email = payload.get("email")
       if not email:
            raise HTTPException(status_code=404,detail="email is not found in the token")
       return email
   except JWTError:
        raise HTTPException(status_code=401,detail="internal server error or invalid token")
 


