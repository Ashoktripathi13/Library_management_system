from fastapi import FastAPI,HTTPException,Depends
from  pydantic import BaseModel,Field
from typing import Dict,List,Optional
from datetime import date, datetime

class UserCreate(BaseModel):
    Name:str
    Email:str
    MembershipDate: Optional[datetime]

class BookCreate(BaseModel):
    Title:str
    ISBN:str
    PublishedDate:Optional[date]
    Genre:str

class BookDetailsUpdate(BaseModel):
    NumberOfPages:int
    Publisher:str
    Language:str

class UpdateResponse(BaseModel):
    message: str
    NumberOfPages:int
    Publisher:str
    Language:str
    



