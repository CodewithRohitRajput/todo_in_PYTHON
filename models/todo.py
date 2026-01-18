from pydantic import BaseModel


class todos(BaseModel):
    title : str
    completed : bool = False