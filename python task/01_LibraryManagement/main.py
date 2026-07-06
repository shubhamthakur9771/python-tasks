# # main.py
# from Models.Book import Book
# from Models.Ebook import Ebook
# from Models.PrintedBook import PrintedBook
# from Services import FileManager


# books = {}

# books["101"] = Book(
#     "Python",
#     "ABC",
#     "101",
#     False,
#     5
# )

# books["102"] = Ebook(
#     "AI",
#     "XYZ",
#     "102",
#     25.5,
#     True,
#     10
# )

# books["103"] = PrintedBook(
#     "C++",
#     "John",
#     "103",
#     "A-12",
#     False,
#     2
# )

# fm = FileManager()

# fm.save_books(books)

# loaded = fm.load_books()

# for book in loaded.values():

#     print(type(book).__name__)

#     print(book.title)
#     print(book.author)
#     print(book.isbn)
#     print(book.is_borrowed)
#     print(book.borrow_count)

#     if isinstance(book, Ebook):
#         print(book.file_size)

#     if isinstance(book, PrintedBook):
#         print(book.shelf_number)

#     print()



from Models.Book import Book
from Models.Ebook import Ebook
from Models.PrintedBook import PrintedBook
from Services.Library import Library


def menu():
    print("\n========== LIBRARY MANAGEMENT ==========")
    print("1. Add Book")
    print("2. Add Ebook")
    print("3. Add Printed Book")
    print("4. Display All Books")
    print("5. Borrow Book")
    print("6. Return Book")
    print("7. Search Book by Title")
    print("8. Remove Book")
    print("9. Display Books Sorted by Title")
    print("10. Display Ebooks Sorted by File Size")
    print("11. Borrow Summary")
    print("0. Exit")
    print("========================================")


library = Library()

while True:
    menu()

    choice = input("Enter your choice: ")

    if choice == "1":
        title = input("Title: ")
        author = input("Author: ")
        isbn = input("ISBN: ")

        book = Book(title, author, isbn)
        library.add_book(book)

    elif choice == "2":
        title = input("Title: ")
        author = input("Author: ")
        isbn = input("ISBN: ")
        file_size = float(input("File Size (MB): "))

        ebook = Ebook(title, author, isbn, file_size)
        library.add_book(ebook)

    elif choice == "3":
        title = input("Title: ")
        author = input("Author: ")
        isbn = input("ISBN: ")
        shelf = input("Shelf Number: ")

        printed_book = PrintedBook(title, author, isbn, shelf)
        library.add_book(printed_book)

    elif choice == "4":
        library.display_books()

    elif choice == "5":
        isbn = input("Enter ISBN: ")
        library.borrow_book(isbn)

    elif choice == "6":
        isbn = input("Enter ISBN: ")
        library.return_book(isbn)

    elif choice == "7":
        title = input("Enter title to search: ")
        library.search_by_title(title)

    elif choice == "8":
        isbn = input("Enter ISBN: ")
        library.remove_book(isbn)

    elif choice == "9":
        library.display_books_sorted_by_title()

    elif choice == "10":
        library.display_ebooks_sorted_by_file_size()

    elif choice == "11":
        library.display_borrow_summary()

    elif choice == "0":
        print("Thank you for using Library Management System.")
        break

    else:
        print("Invalid choice. Try again.")