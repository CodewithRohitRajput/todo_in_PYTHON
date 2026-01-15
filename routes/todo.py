from fastapi import APIRouter, HTTPException
from bson import objectid
from config.mongodb import todo_collection
from models.todo import todos

router = APIRouter()

@router.post("/")
async def create_todo(todo : todos):
    result = await todo_collection.insert_one(todo.dict())
    return{
        "id" : str(result.inserted_id),
        "title" : todo.title,
    }

@router.get("/")
async def get_todos():
    todos = []

    async for i in todo_collection.find():
         i["_id"] = str(i["_id"])
         todos.append(i)

    return todos