from fastapi import FastAPI
from .models import Base, engine
from .routers import book_router

# Создаем экземпляр FastAPI
app = FastAPI()

# Создаем все таблицы в базе данных
Base.metadata.create_all(bind=engine)

# Подключаем маршруты
app.include_router(book_router)
