class Book:
  def __init__(self, title, author,isbn, is_borrowed = False, borrow_count = 0):
    self.title = title
    self.author = author
    self.isbn = isbn
    self.is_borrowed = is_borrowed
    self.borrow_count = borrow_count

  

  def display_info(self):
    print(f"Book : Book | Title : {self.title} | Author : {self.author} | ISBN : {self.isbn} | Borrowed : {self.is_borrowed} | Borrow count : {self.borrow_count}")
  
