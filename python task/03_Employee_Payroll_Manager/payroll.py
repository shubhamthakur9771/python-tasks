from sorting import bubble_sort
from grouping import department_average
from file_handler import write_payslips
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
def process_payroll(employees):
    print("\n Employees Before Sorting\n")

    for emp in employees:
        print(emp)
    bubble_sort(employees)

    print("\n Employees After Sorting\n")

    for emp in employees:
        print(emp)

    department_average(employees)
    write_payslips(os.path.join(BASE_DIR, "payslips.txt"), employees)
    print("\nPayslips Generated Successfully.")