from employee import Employee

    
class Manager(Employee):
    def __init__(self, name, emp_id ,base_salary, department, team_size = 10, bonus_percent = 20):
        super().__init__(name,emp_id, base_salary)
        self.department = department
        self.team_size = team_size
        self.bonus_percent = bonus_percent

    def calculate_salary(self):
        bonus = self.base_salary*self.bonus_percent/100
        return self.base_salary + bonus