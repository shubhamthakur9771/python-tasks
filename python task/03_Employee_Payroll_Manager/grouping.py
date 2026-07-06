def department_average(employees):
    dept = {}
    for emp in employees:
        if emp.department not in dept:
            dept[emp.department] = [0, 0]
        dept[emp.department][0] += emp.calculate_salary()
        dept[emp.department][1] += 1
    print("\nDepartment Wise Average Salary\n")

    for d in dept:
        total = dept[d][0]
        count = dept[d][1]
        print(d, ":", round(total/count, 2))