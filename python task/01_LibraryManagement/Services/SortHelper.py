from Models import Book, Ebook

class SortHelper:

  def sort_by_title(self, books:dict[str, Book]) -> list[Book]:
    book_list = []
    for book in books.values():
      book_list.append(book)
    
    # Bubble sort
    for i in range(len(book_list)-1):
      for j in range(len(book_list) -i - 1):
        if book_list[j].title > book_list[j+1].title:
          book_list[j], book_list[j+1] = book_list[j+1], book_list[j]
        
    return book_list
  
  def sort_by_file_size(self, books:dict[str,Book]) -> list[Ebook]:
    ebook_list = []
    for book in books.values():
      if isinstance(book, Ebook):
        ebook_list.append(book)

    # Bubble Sort

    for i in range(len(ebook_list) - 1):
      for j in range(len(ebook_list)- i - 1):
        if ebook_list[j].file_size > ebook_list[j+1].file_size:
          temp = ebook_list[j]
          ebook_list[j] = ebook_list[j+1]
          ebook_list[j+1] = temp
    return ebook_list

  def borrow_summary(self,books: dict[str, Book]):
    total_books = len(books)
    borrowed_books = 0
    book_list = []

    for book in books.values():
      book_list.append(book)

      if book.is_borrowed:
        borrowed_books += 1

    for i in range(len(book_list) - 1):
      for j in range(len(book_list)- i - 1):
        if book_list[j].borrow_count < book_list[j+1].borrow_count:
          temp = book_list[j]
          book_list[j] = book_list[j+1]
          book_list[j+1] = temp

    print("Borrow summary: ")
    print(f"Total Books : {total_books}")
    print(f"Total Borrowed Books : {borrowed_books}")
    print("Top 3 most Borrowed")

    limit = min(3, len(book_list))
    for i in range(limit):
      print(f"{i +1}. {book_list[i].title} (Borrowed {book_list[i].borrow_count} times)")