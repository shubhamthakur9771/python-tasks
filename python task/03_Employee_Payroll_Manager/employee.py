class Employee:
    def __init__(self,name, emp_id,base_salary):
        self.name = name
        self.emp_id = emp_id
        self.base_salary = float(base_salary)

    def calculate_salary(self):
        return self.base_salary
    
    def __str__(self):
        return f"{self.emp_id} - {self.name} - {self.calculate_salary():.2f}"

    