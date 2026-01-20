from fastapi import APIRouter, HTTPException,Depends
from bson import ObjectId
from config.mongodb import todo_collection
from models.todo import todos
from security import get_current_user


router = APIRouter()




@router.get("/protected")
async def protected_route(cuser : str = Depends(get_current_user)):
    return {"message" : "hey man this is the protected route"}



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



@router.delete("/{id}")
async def delete_todo(id : str):
    todo = await todo_collection.find_one({"_id" : ObjectId(id)})
    if not todo:
        raise HTTPException(status_code=404, detail="Todo no found bruh")
    t = todos(**todo)
    result =   await todo_collection.delete_one({"_id" : ObjectId(id)})
    return {"message " : f"todo deleted : {t.title}"}



@router.put("/{id}")
async def update_todo(id : str , todo : todos):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=404, detail="Todo not found")

    result = await todo_collection.update_one(
        {"_id" : ObjectId(id)},
        {"$set" : todo.dict()}
    )

    return {"message" : f"{todo.title} ->  Updated"}

