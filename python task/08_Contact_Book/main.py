from contact import Contact
from contact_manager import ContactManager

manager = ContactManager()

while True:

    print("\n1.Add")
    print("2.Load")
    print("3.Display")
    print("4.Search")
    print("5.Duplicates")
    print("6.Save")
    print("7.Exit")

    choice = input("Choice : ")

    if choice == "1":

        name = input("Name : ")
        phone = input("Phone : ")
        email = input("Email : ")
        category = input("Category : ")

        manager.add_contact(
            Contact(name, phone, email, category)
        )

    elif choice == "2":

        manager.load_contacts()

    elif choice == "3":

        manager.display_contacts()

    elif choice == "4":

        name = input("Enter Name : ")

        result = manager.binary_search(name)

        if result:
            result.display()
        else:
            print("Not Found")

    elif choice == "5":

        duplicates = manager.find_duplicates()

        if duplicates:

            for d in duplicates:
                print(d)

        else:
            print("No Duplicate Phone Numbers")

    elif choice == "6":

        manager.save_contacts()

    elif choice == "7":

        break