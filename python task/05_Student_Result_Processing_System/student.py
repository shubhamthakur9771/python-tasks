class Student:
    def __init__(self,roll_no, name, sub1, sub2, sub3):
        self.roll_no = roll_no
        self.name = name
        self.sub1 = sub1
        self.sub2 = sub2
        self.sub3 = sub3

    def total(self):
        return self.sub1 + self.sub2 + self.sub3
    
    def average(self):
        return self.total()/3
    
    def is_pass(self):
        return (self.sub1 >= 35 and self.sub2 >= 35 and self.sub3 >= 35)
    
    def get_grade(self):
        avg = self.average()
        if avg >= 90:
            return "A+"
        elif(avg >= 80):
            return "A"
        elif(avg >= 70):
            return "B"
        elif(avg >= 60):
            return "C"
        elif(avg >= 50):
            return "D"
        elif(avg >= 35):
            return "E"
        else:
            return "F"
        
    
    
        

