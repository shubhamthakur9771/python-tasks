import os
from Models import Book, Ebook, PrintedBook
class FileManager:
  def __init__(self):
    current_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    self.filepath = os.path.join(current_folder,"Data", "Library.txt")

  def save_books(self, books):
    lines = []
    for book in books.values():
      if isinstance(book, Ebook):
        line = (f"EBOOK|{book.title}|{book.author}|{book.isbn}|{book.file_size}|{book.is_borrowed}|{book.borrow_count}")
      elif isinstance(book, PrintedBook):
        line = (f"PRINTEDBOOK|{book.title}|{book.author}|{book.isbn}|{book.shelf_number}|{book.is_borrowed}|{book.borrow_count}")
      elif isinstance(book, Book):
        line = (f"BOOK|{book.title}|{book.author}|{book.isbn}|{book.is_borrowed}|{book.borrow_count}")
      lines.append(line)
    with open(self.filepath, "w") as file:
      file.write("\n".join(lines))
  
  def load_books(self):
    books = {}

    if not os.path.exists(self.filepath):
      return books
    with open(self.filepath, "r") as file:
      for line in file:
        line = line.strip()
        try:
          data = line.split("|")
          if data[0] == "BOOK":
            book = Book(
              title = data[1],
              author = data[2],
              isbn = data[3],
              is_borrowed = bool(data[4]),
              borrow_count = int(data[5])
            )
            books[book.isbn] = book

          elif data[0] == "EBOOK":
            ebook = Ebook(
              title = data[1],
              author = data[2],
              isbn = data[3],
              file_size = float(data[4]),
              is_borrowed = bool(data[5]),
              borrow_count = int(data[6]),
            )
            books[ebook.isbn] = ebook
          elif data[0] == "PRINTEDBOOK":
            printed_book = PrintedBook(
              title = data[1],
              author = data[2],
              isbn = data[3],
              shelf_number = data[4],
              is_borrowed = bool(data[5]),
              borrow_count = int(data[6])
            )
            books[printed_book.isbn] = printed_book

        except Exception:
          print("Invalid line skipped: ", line)
    return books
  

