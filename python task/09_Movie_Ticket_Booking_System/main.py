from cinema import Cinema
from show import Show

cinema = Cinema()

show1 = Show("Avengers", "10:00 AM", 5, 6)
show2 = Show("Bahubali", "2:00 PM", 5, 6)
show3 = Show("Pushpa", "6:00 PM", 5, 6)

cinema.add_show(show1)
cinema.add_show(show2)
cinema.add_show(show3)

cinema.load_bookings()

while True:

    print("\n========== MOVIE BOOKING SYSTEM ==========")
    print("1. Display Shows")
    print("2. Display Seats")
    print("3. Book Ticket")
    print("4. Cancel Booking")
    print("5. Find Best Block")
    print("6. Sort Shows By Occupancy")
    print("7. Display Bookings")
    print("8. Exit")

    choice = int(input("Enter choice : "))

    if choice == 1:

        cinema.display_shows()

    elif choice == 2:

        cinema.display_shows()

        show_number = int(input("Enter show number : "))

        cinema.shows[show_number - 1].display_seats()

    elif choice == 3:

        cinema.display_shows()

        show_number = int(input("Enter show number : "))

        customer = input("Enter customer name : ")

        count = int(input("How many seats : "))

        seats = []

        for i in range(count):

            print("Seat", i + 1)

            row = int(input("Row : "))
            col = int(input("Column : "))

            seats.append((row, col))

        cinema.book_ticket(show_number, customer, seats)

    elif choice == 4:

        name = input("Enter customer name : ")

        cinema.cancel_booking(name)

    elif choice == 5:

        cinema.display_shows()

        show_number = int(input("Enter show number : "))

        n = int(input("Number of consecutive seats : "))

        seats = cinema.find_best_block(show_number, n)

        if len(seats) == 0:
            print("No consecutive seats found.")
        else:
            print("Best Block :", seats)

    elif choice == 6:

        cinema.sort_shows()

        print("Shows Sorted Successfully.")

    elif choice == 7:

        cinema.display_bookings()

    elif choice == 8:

        print("Thank You")

        break

    else:

        print("Invalid Choice")