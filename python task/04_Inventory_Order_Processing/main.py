from inventory import Inventory
from stack import Stack
from queue import Queue

inventory = Inventory()
inventory.load_stock()

undo_stack = Stack()

shipping_queue = Queue()

while True:

    print("\n===== INVENTORY SYSTEM =====")

    print("1. View Products")

    print("2. Place Order")

    print("3. Undo Last Order")

    print("4. Ship Order")

    print("5. View Pending Orders")

    print("6. Low Stock Alert")

    print("7. Find Products By Budget")

    print("8. Exit")

    choice = input("Enter Choice : ")

    if choice == "1":

        inventory.display_products()

    elif choice == "2":

        inventory.place_order(undo_stack, shipping_queue)

    elif choice == "3":

        inventory.undo_last_order(undo_stack)

    elif choice == "4":

        inventory.ship_order(shipping_queue)

    elif choice == "5":

        shipping_queue.display()

    elif choice == "6":

        inventory.low_stock_alert()

    elif choice == "7":

        budget = float(input("Enter Budget : "))

        pair = inventory.closest_products(budget)

        if pair:

            p1, p2, total = pair

            print("\nRecommended Products")

            print(p1)

            print(p2)

            print("Total =", total)

    elif choice == "8":

        print("Thank You")

        break

    else:

        print("Invalid Choice")