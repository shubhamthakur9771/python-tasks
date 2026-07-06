from student import Student
from logger import Logger
import os

class ResultProcessor:
    def __init__(self):
        self.students = []

    def load_results(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(base_dir,"results.txt")
        with open(filename,"r") as file:
            for line in file:
                data = line.strip().split(",")
                if(len(data) != 5):
                    Logger.log(f"Skipped Record --> {line.strip()} : Missing Fields")
                    continue
                try:
                    roll = data[0]
                    name = data[1]
                    sub1 = int(data[2])
                    sub2 = int(data[3])
                    sub3 = int(data[4])

                    student = Student(roll, name, sub1, sub2, sub3)
                    self.students.append(student)
                except ValueError:
                    Logger.log(f"Skipped Record --> {line.strip()} : Non-numeric marks")


    def rank_students(self):
        n = len(self.students)

        for i in range(n):
            for j in range(0, n- i -1):
                if self.students[j].total() < self.students[j+1].total():
                    temp = self.students[j]
                    self.students[j] = self.students[j+1]
                    self.students[j+1] = temp
        

    def class_average(self):
        n = len(self.students)
        if n == 0:
            return 0
        total = 0
        for student in self.students:
            total += student.total()
        avg = total/n
        return avg
    
    def topper(self):
        n = len(self.students)
        if n == 0:
            return None
        return self.students[0]

    def pass_percentage(self):
        total = len(self.students)
        if total == 0:
            return
        pass_count = 0
        for student in self.students:
            if student.is_pass():
                pass_count += 1
        return (pass_count/total)* 100
    


    def generate_report_cards(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        reportcard_dir = os.path.join(base_dir,"reportcards")
        os.makedirs(reportcard_dir, exist_ok=True)

        for student in self.students:
            # filename = "reportcards/" + student.roll_no + ".txt"
            filename = os.path.join(reportcard_dir,student.roll_no + ".txt")
            with open(filename,"w") as file:
                file.write("===== Report Card =====\n\n")
                file.write(f"Roll No : {student.roll_no}\n")
                file.write(f"Name     : {student.name}\n\n")
                file.write(f"Subject 1 : {student.sub1}\n")
                file.write(f"Subject 2 : {student.sub2}\n")
                file.write(f"Subject 3 : {student.sub3}\n\n")

                file.write(f"Total : {student.total()}\n")
                file.write(f"Average : {student.average():.2f}\n")
                file.write(f"Grade : {student.get_grade()}\n")

                if student.is_pass():
                    file.write("Result : PASS\n")
                else:
                    file.write("Result : FAIL\n")


