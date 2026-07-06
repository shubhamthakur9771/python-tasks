from .Book import Book
class Ebook(Book):
  def __init__(self,title, author, isbn,  file_size, is_borrowed = False, borrow_count = 0):
    super().__init__(title, author, isbn, is_borrowed, borrow_count)
    self.file_size = file_size
  
  def display_info(self):
    print(f"Book Type : Ebook | Title : {self.title} | Author | {self.author} | ISBN : {self.isbn} | File Size : {self.file_size} | Borrowed : {self.is_borrowed} | Borrow Count : {self.borrow_count}")