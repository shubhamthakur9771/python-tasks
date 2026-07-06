from show import Show
class Booking:
    def __init__(self,customer_name,show,seat_numbers):
        self.customer_name = customer_name
        self.show = show
        self.seat_numbers = seat_numbers

    def __str__(self):
        return f"Customer Name : {self.customer_name} | Show : {self.show} | Seat Number : {self.seat_numbers}"
    
    def display_booking(self):
        print(f"Customer : {self.customer_name} | Movie : {self.show.movie_name} | Time : {self.show.time} | Seats : {self.seat_numbers}")

    