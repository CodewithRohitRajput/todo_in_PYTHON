from fastapi import APIRouter, HTTPException, Response
from models.user import users
from security import hashpass, verifypass,create_access_token
from config.mongodb import user_collection



router = APIRouter(prefix='/auth', tags=["Auth"])

@router.post("/signup")
async def signup(user : users):
    existingUser = await user_collection.find_one({"email" : user.email})
    if existingUser:
        raise HTTPException(status_code=400, detail="user is already signedIn")
    
    hashed_pass = hashpass(user.password)

    await user_collection.insert_one({"username" : user.username , "email" : user.email , "password" : hashed_pass})
    
    token = create_access_token({"email" : user.email})
    response = Response(
        content=f'{{"message": "User successfully created", "access_token": "{token}", "token_type": "bearer"}}',
        media_type="application/json"
    )
    response.set_cookie(key="access_token", value=token, httponly=True)
    return response


@router.post("/login")
async def login(user : users):
    isUser = await user_collection.find_one({"email" : user.email})
    if not isUser:
        raise HTTPException(status_code=404, detail="user not found")
    isPass =  verifypass(user.password , isUser["password"])

    if not isPass:
        raise HTTPException(status_code=404, detail="password is wrong, correct password is : ")
    
    token = create_access_token({"email" : user.email})
    response = Response(
        content='{"message": "Login successful"}',
        # media_type="application/json"
    )
    response.set_cookie(key="access_token", value=token, httponly=True)
    return response