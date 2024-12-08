import base64
import hashlib
import hmac
import json
from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from models import Book, User
from schemas import BookCreate, Book as BookSchema, UserCreate, User as UserSchema
from database import engine, SessionLocal, Base, get_db
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

SECRET_KEY = "mysecret"

def create_token(payload: dict) -> str:
    header = json.dumps({"alg": "HS256", "typ": "JWT"}).encode()
    payload = json.dumps(payload).encode()

    header_b64 = base64.urlsafe_b64encode(header).decode().rstrip("=")
    payload_b64 = base64.urlsafe_b64encode(payload).decode().rstrip("=")

    signature = hmac.new(SECRET_KEY.encode(), f"{header_b64}.{payload_b64}".encode(), hashlib.sha256).digest()
    signature_b64 = base64.urlsafe_b64encode(signature).decode().rstrip("=")

    return f"{header_b64}.{payload_b64}.{signature_b64}"

def decode_token(token: str) -> dict:
    header_b64, payload_b64, signature_b64 = token.split(".")
    signature_check = hmac.new(SECRET_KEY.encode(), f"{header_b64}.{payload_b64}".encode(), hashlib.sha256).digest()
    signature_check_b64 = base64.urlsafe_b64encode(signature_check).decode().rstrip("=")

    if signature_check_b64 != signature_b64:
        raise HTTPException(status_code=401, detail="Invalid token signature")

    payload_json = base64.urlsafe_b64decode(payload_b64 + "==").decode()
    return json.loads(payload_json)

async def get_current_user(token: str = Header(None)) -> dict:
    if not token:
        raise HTTPException(status_code=401, detail="Token is missing")

    try:
        payload = decode_token(token)
        return payload
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token validation failed: {str(e)}")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# @app.post("/token")
# def generate_token(data: dict):
#     token = create_token(data)
#     return {"token": token}

@app.post("/users/create", response_model=UserSchema)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(username=user.username, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/users/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username, User.password == user.password).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    token = create_token({"username": user.username})
    return {"token": token}

@app.post("/books/add", response_model=BookSchema)
def create_book(book: BookCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_book = Book(title=book.title, author=book.author, description=book.description)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@app.get("/books/get", response_model=list[BookSchema])
def read_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    books = db.query(Book).offset(skip).limit(limit).all()
    return books

@app.get("/books/{book_id}", response_model=BookSchema)
def read_book(book_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@app.delete("/books/{book_id}", response_model=BookSchema)
def delete_book(book_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(db_book)
    db.commit()
    return db_book

@app.put("/books/{book_id}", response_model=BookSchema)
def update_book(book_id: int, book: BookCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    db_book.title = book.title
    db_book.author = book.author
    db_book.description = book.description
    db.commit()
    db.refresh(db_book)
    return db_book

# @app.get("/books/search", response_model=list[BookSchema])
# def search_books(title: str = None, author: str = None, db: Session = Depends(get_db)):
#     query = db.query(Book)
#     if title:
#         query = query.filter(Book.title.ilike(f"%{title}%"))
#     if author:
#         query = query.filter(Book.author.ilike(f"%{author}%"))
#     books = query.all()
#     return books
#
# @app.get("/books/all", response_model=list[BookSchema])
# def get_all_books(db: Session = Depends(get_db)):
#     books = db.query(Book).all()
#     return books
