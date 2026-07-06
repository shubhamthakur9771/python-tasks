from booking import Booking
import os
import ast
class Cinema:
    def __init__(self):
        self.shows = []
        self.bookings = []
    
    def add_show(self,show):
        self.shows.append(show)

    def display_shows(self):
        if len(self.shows) == 0:
            print("No shows available")
            return
        for i in range(len(self.shows)):
            show = self.shows[i]
            print(f"Show Number : {i+1}, Movie Name : {show.movie_name}, Time : {show.time}, Total Seats : {show.total_seats}, Booked Seats : {show.booked_seats}")
            occupancy = (show.booked_seats / show.total_seats) * 100

            print("Occupancy :", round(occupancy,2), "%")
            print("-"*30)

    def book_ticket(self,show_number, customer_name, seat_numbers):
        show = self.shows[show_number-1]
        for seat in seat_numbers:
            row = seat[0]
            col = seat[1]
            if row < 0 or row >= show.rows:
                print("Invalid Row : ", row)
                return
            if col < 0 or col >= show.cols:
                print("Invalid column : ", col)
                return
            if show.seat_matrix[row][col] == "B":
                print("Seat ", seat , " is already booked.")
                return
        for seat in seat_numbers:
            row = seat[0]
            col = seat[1]
            show.seat_matrix[row][col] = "B"
            show.booked_seats += 1
        booking = Booking(customer_name, show, seat_numbers)
        self.bookings.append(booking)
        self.save_booking(booking)
        print("Booking Successful")
        
    def cancel_booking(self,customer_name):
        found = False
        for booking in self.bookings:
            if booking.customer_name == customer_name:
                show = booking.show
                for seat in booking.seat_numbers:
                    row = seat[0]
                    col = seat[1]
                    show.seat_matrix[row][col] = "A"
                    show.booked_seats -= 1
                self.bookings.remove(booking)
                self.update_booking_file()
                print("Booking cancelled")
                found = True
                break
        if found == False:
            print("Booking Not Found")

    def save_booking(self, booking):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(base_dir,"bookings.txt")
        with open(filename,"a") as file:
            file.write(f"{booking.customer_name},{booking.show.movie_name},{str(booking.seat_numbers)}\n")

    def update_booking_file(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(base_dir,"bookings.txt")
        with open(filename,"w") as file:
            for booking in self.bookings:
                file.write(f"{booking.customer_name},{booking.show.movie_name},{str(booking.seat_numbers)}\n")

    def find_best_block(self,show_number,n):
        show = self.shows[show_number-1]
        for row in range(show.rows):
            count = 0
            for col in range(show.cols):
                if show.seat_matrix[row][col] == "A":
                    count +=1
                else:
                    count =0
                if count == n:
                    seats = []
                    start = col - n + 1
                    for i in range(start,col+1):
                        seats.append((row,i))
                    return seats
        return []
    
    def sort_shows(self):
        size = len(self.shows)
        for i in range(size):
            for j in range(size-i-1):
                show1 = self.shows[j]
                show2 = self.shows[j+1]

                occ1 = show1.booked_seats/show1.total_seats
                occ2 = show2.booked_seats/show2.total_seats

                if occ1 < occ2:
                    self.shows[j], self.shows[j+1] = self.shows[j+1], self.shows[j]


    def display_bookings(self):
        if len(self.bookings) == 0:
            print("No Bookings Found.")
            return
        for booking in self.bookings:
            print(f"Customer : {booking.customer_name} | Movie : {booking.show.movie_name} | Seats : {booking.seat_numbers}")
            print("-"*30)

    def load_bookings(self):
        self.bookings.clear()
        try:

            base_dir = os.path.dirname(os.path.abspath(__file__))
            filename = os.path.join(base_dir,"bookings.txt")
            with open(filename,"r") as file:
                for line in file:
                    data = line.strip().split(",",2)
                    if len(data) != 3:
                        print("Invalid booking : ", line.strip())
                        continue
                    customer_name = data[0]
                    movie_name = data[1]

                    try:
                        seat_numbers = ast.literal_eval(data[2])
                    except:
                        print("Invalid seat data : ", line.strip())
                        continue

                    selected_show = None
                    for show in self.shows:
                        if show.movie_name == movie_name:
                            selected_show = show
                            break
                    if selected_show is None:
                        print("Show not found : " , movie_name)
                        continue
                    valid = True
                    for seat in seat_numbers:
                        row = seat[0]
                        col = seat[1]

                        if row < 0 or row >= selected_show.rows:
                            valid = False
                            break
                        if col < 0 or col >= selected_show.cols:
                            valid = False
                            break
                    if valid == False:
                        print("Invalid seat position : ", line.strip())
                        continue
                    for seat in seat_numbers:
                        row = seat[0]
                        col = seat[1]

                        selected_show.seat_matrix[row][col] = "B"
                        selected_show.booked_seats += 1

                    booking = Booking(customer_name, selected_show,seat_numbers)
                    self.bookings.append(booking)
        except FileNotFoundError:
            print("bookings.txt not found")
                



                

                




    
            