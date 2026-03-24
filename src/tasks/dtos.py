from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# This is a schema where data will be come from postman 
class TaskSchema(BaseModel):
    title:str
    description:str
    is_completed:bool=False
    priority:str="medium"
    due_date:Optional[datetime]=None


class TaskResponseSchema(BaseModel):
    id:int
    title:str
    description:str
    is_completed:bool=False
    priority:str="medium"
    due_date:Optional[datetime]=None
    created_at:Optional[datetime]=None
    user_id:int | None = 0 
 
    



class MultipleCond(BaseModel):
    title:str
    is_completed:bool

# Request flow 

"""
Request flow:
Request coming from postman 
request-->dtos-->router-->controller-->models-->save In Database
"""
 