from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional, List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .models import Post
from .connect_database import engine, get_db
from .routers import posts, users, authentication

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def connect_database():
    try:
        conn = psycopg2.connect(host='localhost', port=5432, database='FastAPI_database', user='postgres', password='Krishnas5#',
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection established!!")
        return conn, cursor
    except Exception as error:
        print("Database connection error")
        print("error: %s" % error)
        time.sleep(2)


conn, cursor = connect_database()


my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "favourite food", "content": "I love pizza", "id": 2}]
# Magical decorator (very important for API calling)


def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p


def find_index(id):
    for i in range(0, len(my_posts)):
        if my_posts[i]['id'] == id:
            return i


app.include_router(posts.router)
app.include_router(users.router)
app.include_router(authentication.router)

@app.get("/")  # Path operations (all lines of code fo this passage)
# "/" is the root path of the website [eg. - if the path = "/login" then the website = http://127.0.0.1:8086/login]
async def read_root():  # async (is optional / when we cgonna perform a long task that time we usually need)
    # Retun an json universal for web
    return {"Hello": "Welcome to our API !!!!"}





