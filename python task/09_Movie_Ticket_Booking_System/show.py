class Show:
    def __init__(self,movie_name,time,rows,cols):
        self.movie_name = movie_name
        self.time = time
        self.rows = rows
        self.cols = cols

        self.total_seats = rows * cols
        self.booked_seats = 0

        self.seat_matrix = [['A' for _ in range(cols)] for _ in range(rows)]

    def __str__(self):
        return f"Movie Name : {self.movie_name} | Time : {self.time} Total Seats : {self.total_seats} | Booked Seats : {self.booked_seats}"
    
    def display_seats(self):
        for row in self.seat_matrix:
            for seat in row:
                print(seat, end=" ")
            print()

    
