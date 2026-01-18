from motor.motor_asyncio import AsyncIOMotorClient

moongo_url = "mongodb://localhost:27017"

client = AsyncIOMotorClient(moongo_url)

database = client.todos_td

todo_collection = database.todo
user_collection = database.user