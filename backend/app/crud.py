from sqlalchemy.orm import Session
from . import models, schemas

def get_books(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Book).offset(skip).limit(limit).all()

def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(title=book.title, author=book.author)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def delete_book(db: Session, book_id: int):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if book:
        db.delete(book)
        db.commit()
    return book

def update_book(db: Session, book_id: int, book_data: schemas.BookCreate):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if book:
        book.title = book_data.title
        book.author = book_data.author
        db.commit()
        db.refresh(book)
    return book
