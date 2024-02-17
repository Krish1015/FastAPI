from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import Optional, List
from .. import models, schemas, utils, Oauth2
from ..connect_database import get_db


router = APIRouter(prefix="/posts", tags=["Posts"])

@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db),current_user: int = Depends(Oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts """)
    # my_posts = cursor.fetchall()
    my_posts = db.query(models.Post).all()
    print(my_posts)
    return my_posts  # Take from my_posts


# Post request
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(new_post: schemas.PostCreate, db: Session = Depends(get_db), current_user = Depends(Oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """,
    #              (new_post.title, new_post.content, new_post.published))
    # post = cursor.fetchone()
    # conn.commit()
    print(current_user.email)
    post = models.Post(**new_post.dict())
    db.add(post)
    db.commit()
    db.refresh(post)

    return post
# title:string, content:string


@router.get("/{id}", response_model=schemas.Post)
def get_one_post(id: int, response: Response, db: Session = Depends(get_db),current_user: int = Depends(Oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """,
    #              (str(id),))
    post = db.query(models.Post).filter(models.Post.id == id).first()
    # print(type(id))
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post not found with id {id}")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Post not found with id {id}"}
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),current_user: int = Depends(Oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s returning *""",
    #               (str(id),))
    # deleted_post = cursor.fetchone()
    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    if not deleted_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post not found with id {id}")
    # conn.commit()
    deleted_post.delete(synchronize_session=False)
    db.commit()
    return {"message": f"Post deleted with id {id}"}


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db),current_user: int = Depends(Oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s returning *""",
    #               (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    updated_post = db.query(models.Post).filter(models.Post.id == id)

    if not updated_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post not found with id {id}")
    # conn.commit()
    updated_post.update(post.dict(), synchronize_session=False)
    db.commit()
    return updated_post.first()