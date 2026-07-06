from file_handler import read_employees
from payroll import process_payroll
import os


def menu():

    employees = []

    while True:

        print("\n========== Employee Payroll ==========")
        print("1. Load Employees")
        print("2. Process Payroll")
        print("3. Exit")

        choice = input("Enter choice: ")

        if choice == "1":

            # employees = read_employees("employees.txt")
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            EMPLOYEE_FILE = os.path.join(BASE_DIR, "employees.txt")
            employees = read_employees(EMPLOYEE_FILE)

            print(len(employees), "Employees Loaded")

        elif choice == "2":

            if len(employees) == 0:
                print("Load employee data first.")
            else:
                process_payroll(employees)

        elif choice == "3":

            print("Thank You")
            break

        else:
            print("Invalid Choice")


menu()