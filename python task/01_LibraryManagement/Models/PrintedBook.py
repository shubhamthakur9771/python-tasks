from .Book import Book
class PrintedBook(Book):
  def __init__(self, title, author, isbn, shelf_number, is_borrowed = False, borrow_count = 0):
    super().__init__(title, author, isbn, is_borrowed, borrow_count)
    self.shelf_number = shelf_number

  def display_info(self):
    print(f"Book : Printed Book | Title : {self.title} | Author : {self.author} | ISBN : {self.isbn} | Self Number : {self.shelf_number} | Borrowed : {self.is_borrowed} | Borrow count : {self.borrow_count}")
