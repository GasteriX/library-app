from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Book  # Импортируем модель Book
from schemas import BookCreate, Book as BookSchema  # Импортируем схемы для валидации
from database import engine, SessionLocal, Base  # Импортируем Base
from fastapi.middleware.cors import CORSMiddleware

# Создаем экземпляр FastAPI
app = FastAPI()

# Разрешаем доступ только с вашего React-приложения
origins = [
    "http://localhost:3000",  # Ваше React-приложение
    "http://127.0.0.1:3000",  # Для возможных вариантов адреса
]

# Добавляем middleware для обработки CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Разрешаем доступ с этих доменов
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все методы (GET, POST, DELETE и т.д.)
    allow_headers=["*"],  # Разрешаем все заголовки
)


# Создаем таблицы в базе данных
Base.metadata.create_all(bind=engine)  # Используем Base, если это родитель всех моделей

# Получаем сессию базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Добавление книги
@app.post("/books/", response_model=BookSchema)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    db_book = Book(title=book.title, author=book.author, description=book.description)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

# Удаление книги
@app.delete("/books/{book_id}", response_model=BookSchema)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(db_book)
    db.commit()
    return db_book

# Поиск книг по названию или автору
@app.get("/books/", response_model=list[BookSchema])
def search_books(title: str = None, author: str = None, db: Session = Depends(get_db)):
    query = db.query(Book)
    if title:
        query = query.filter(Book.title.ilike(f"%{title}%"))
    if author:
        query = query.filter(Book.author.ilike(f"%{author}%"))
    books = query.all()
    return books
@app.get("/books/all", response_model=list[BookSchema])
def get_all_books(db: Session = Depends(get_db)):
    books = db.query(Book).all()  # Получаем все книги
    return books