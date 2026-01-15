from fastapi import FastAPI
from routes.todo import router
app = FastAPI()

# @app.get("/")
# def home():
#     return {"greetings" : "hello buddy kjhgjghgc"}

app.include_router(router)