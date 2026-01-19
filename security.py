import bcrypt
from jose import jwt
from datetime import datetime,timedelta

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
    if not isinstance(password, str):
        password = str(password)
    
    password_bytes = password.encode('utf-8')
    
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
    
    # Encode hashed password to bytes (this should always happen, not inside the if)
    hashed_bytes = hashed.encode('utf-8')
    
    return bcrypt.checkpw(password_bytes, hashed_bytes)




def create_access_token(data : dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
    to_encode.update({"exp" : expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    


