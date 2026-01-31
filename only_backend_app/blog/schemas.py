from pydantic import BaseModel, ConfigDict
from typing import List

class User(BaseModel):
    
    name: str
    email: str
    password: str

    model_config = ConfigDict(from_attributes=True)

class BlogBase(BaseModel):

    title: str
    body: str

class Blog(BlogBase):
    model_config = ConfigDict(from_attributes=True)

class ShowUser(BaseModel):
    name: str
    email: str
    blogs: List[Blog] = []
    
class ShowBlog(BlogBase):
    user: ShowUser
    model_config = ConfigDict(from_attributes=True)


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str|None = None