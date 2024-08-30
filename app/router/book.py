from fastapi import HTTPException, status, Response, APIRouter
from .. import database, schemas
import os
from fastapi.encoders import jsonable_encoder
import json

router = APIRouter(
    prefix="/book",
    tags=["Books"]
)


BOOK_DATABASE = []
BOOK_FILE = 'book.json'
if os.path.exists(BOOK_FILE):
    with open(BOOK_FILE, "r") as f:
        BOOK_DATABASE = json.load(f)


@router.get("/")
def list_of_books():
    database.cursor.execute("""SELECT * FROM books""")
    books = database.cursor.fetchall()
    return books


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Book)
def add_book(book: schemas.BookCreate):
    database.cursor.execute("""INSERT INTO books (name, price, published) VALUES(%s, %s, %s) RETURNING *""",
                   (book.name, book.price, book.published))
    book = database.cursor.fetchone()
    database.conn.commit()

    json_book = jsonable_encoder(book)
    BOOK_DATABASE.append(json_book)
    with open(BOOK_FILE, "w") as f:
        json.dump(BOOK_DATABASE, f, indent=2)

    return book


@router.get("/{id}")
def get_book(id: int):
    database.cursor.execute("SELECT * FROM books WHERE id = {} ".format((str(id))))
    book_id = database.cursor.fetchone()
    if not book_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Book with id: {id} does not exist")
    return book_id


@router.put("/{id}", status_code=status.HTTP_201_CREATED, response_model=schemas.Book)
def update_book(id: int, book: schemas.BookCreate):
    database.cursor.execute("""UPDATE books SET name = %s, price = %s, published = %s WHERE id = %s RETURNING *""",
                   (book.name, book.price, book.published, str(id)),)
    book = database.cursor.fetchone()
    if book == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Book with id: {id} does not exist")
    database.conn.commit()
    return book


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(id: int):
    database.cursor.execute("""DELETE FROM books WHERE id = {} RETURNING *""".format((str(id))))
    book = database.cursor.fetchone()
    if book == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Book with id: {id} does not exist")
    database.conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

