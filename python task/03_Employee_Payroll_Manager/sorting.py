def bubble_sort(employees):
    n = len(employees)
    for i in range(0,n):
        for j in range(0,n-i-1):
            if employees[j].calculate_salary() > employees[j+1].calculate_salary():
                employees[j], employees[j+1] = employees[j+1], employees[j]
    return employees