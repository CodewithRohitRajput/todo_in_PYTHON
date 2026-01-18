from fastapi import FastAPI
from routes.todo import router as todo_Router
from routes.auth import router as auth_Router
app = FastAPI()

# @app.get("/")
# def home():
# return {"greetings" : "hello buddy"}

app.include_router(todo_Router)
app.include_router(auth_Router)