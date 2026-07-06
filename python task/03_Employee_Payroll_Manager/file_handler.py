from manager import Manager
from exceptions import InvalidEmployeeData
from logger import log_error

def read_employees(filename):
    employees = []
    try:
        with open(filename, "r") as file:
            for line_no, line in enumerate(file,start=1):
                line = line.strip()
                if not line:
                    continue
                try:
                    parts = line.split(",")
                    if len(parts) != 4:
                        raise InvalidEmployeeData("Malformed row")
                    name = parts[0]
                    emp_id = int(parts[1])
                    salary = float(parts[2])
                    department = parts[3]

                    emp = Manager(name, emp_id,salary,department)
                    employees.append(emp)
                except Exception as e:
                    log_error(f"Line {line_no}: {line} --> {e}")

    except FileNotFoundError:
        print("Employee file not found.")
    return employees

def write_payslips(filename, employees):
    with open(filename, "w") as file:
        file.write("------ PAYSLIPS ------\n\n")
        for emp in employees:
            file.write(f"Employee : {emp.name}\n")
            file.write(f"ID       : {emp.emp_id}\n")
            file.write(f"Department : {emp.department}\n")
            file.write(f"Salary   : {emp.calculate_salary():0.2f}\n")
            file.write("-----------------------------\n")
