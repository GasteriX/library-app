import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css"; // Подключаем стили

const App = () => {
  const [books, setBooks] = useState([]);
  const [newBook, setNewBook] = useState({ title: "", author: "" });
  const [searchTerm, setSearchTerm] = useState("");

  const apiBaseUrl = "http://localhost:5000/books";

  useEffect(() => {
    fetchBooks();
  }, []);

  const fetchBooks = async () => {
    try {
      const response = await axios.get(apiBaseUrl);
      setBooks(response.data);
    } catch (error) {
      console.error("Error fetching books:", error);
    }
  };

  const addBook = async () => {
    if (!newBook.title.trim() || !newBook.author.trim()) {
      alert("Название и автор обязательны!");
      return;
    }

    try {
      const response = await axios.post(apiBaseUrl, newBook);
      setBooks([...books, response.data]);
      setNewBook({ title: "", author: "" });
    } catch (error) {
      console.error("Error adding book:", error);
    }
  };

  const deleteBook = async (id) => {
    try {
      await axios.delete(`${apiBaseUrl}/${id}`);
      setBooks(books.filter((book) => book.id !== id));
    } catch (error) {
      console.error("Error deleting book:", error);
    }
  };

  const filteredBooks = books.filter(
    (book) =>
      book.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      book.author.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="app-container">
      <h1 className="title">Библиотека книг</h1>

      <div className="add-book-container">
        <h3>Добавить книгу</h3>
        <input
          type="text"
          placeholder="Название книги"
          value={newBook.title}
          onChange={(e) => setNewBook({ ...newBook, title: e.target.value })}
          className="input"
        />
        <input
          type="text"
          placeholder="Автор"
          value={newBook.author}
          onChange={(e) => setNewBook({ ...newBook, author: e.target.value })}
          className="input"
        />
        <button onClick={addBook} className="btn btn-add">
          Добавить
        </button>
      </div>

      <div className="search-container">
        <h3>Поиск книг</h3>
        <input
          type="text"
          placeholder="Введите название или автора"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="input search-input"
        />
      </div>

      <div className="book-list-container">
        <h3>Список книг</h3>
        {filteredBooks.length > 0 ? (
          <ul className="book-list">
            {filteredBooks.map((book) => (
              <li key={book.id} className="book-item">
                <span className="book-title">{book.title}</span> -{" "}
                <span className="book-author">{book.author}</span>
                <button
                  onClick={() => deleteBook(book.id)}
                  className="btn btn-delete"
                >
                  Удалить
                </button>
              </li>
            ))}
          </ul>
        ) : (
          <p>Нет книг для отображения</p>
        )}
      </div>
    </div>
  );
};

export default App;
