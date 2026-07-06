from Services.FileManager import FileManager
from Services.SortHelper import SortHelper
from Models.Book import Book
from Models.Ebook import Ebook



class Library:

  def __init__(self):
    self.file_manager = FileManager()
    self.sort_helper = SortHelper()
    self.books = self.file_manager.load_books()

  def add_book(self, book: Book):
    if book.isbn in self.books:
      print("Book Already Exists")
      return
    self.books[book.isbn] = book
    self.file_manager.save_books(self.books)
    print("Book Added.")

  def borrow_book(self, isbn : str):
    if isbn not in self.books:
      print("Book not found.")
      return
    book = self.books[isbn]
    
    if book.is_borrowed:
      print("Book Already Borrowed.")
      return
    
    book.is_borrowed = True
    book.borrow_count += 1
    self.file_manager.save_books(self.books)
    print("Borrow Successfull")

  def return_book(self, isbn: str):
    if isbn not in self.books:
      print("Book Not found")
      return
    
    book = self.books[isbn]
    if not book.is_borrowed:
      print("Book was not borrowed")
      return
    
    book.is_borrowed = False
    self.file_manager.save_books(self.books)
    print("Return Successful")

  def search_by_title(self, title: str):
    found = False
    for book in self.books.values():
      if title.lower() in book.title.lower():
        book.display_info()
        found = True

    if not found:
       print("Book not found")

  def display_books(self):
    if len(self.books) == 0:
      print("No book available")
      return

    for book in self.books.values():
      book.display_info()

  def remove_book(self, isbn:str):
    if isbn not in self.books:
      print("Book not found.")
      return
    del self.books[isbn]
    self.file_manager.save_books(self.books)
    print("Book removed")

  def get_books(self):
    return self.books
  
  def display_books_sorted_by_title(self):
    book_list = self.sort_helper.sort_by_title(self.books)
    for book in book_list:
      book.display_info()
    
  def display_ebooks_sorted_by_file_size(self):
    ebook_list = self.sort_helper.sort_by_file_size(self.books)

    for ebook in ebook_list:
      ebook.display_info()

  def display_borrow_summary(self):
    self.sort_helper.borrow_summary(self.books) 

   
