def read_transactions():
    transactions = []
    try:
        with open("transactions.txt", "r") as file:
            for line in file:
                data = line.strip().split(",")
                transactions.append(data)
    except FileNotFoundError:
        print("No transactions found")
    return transactions

def sort_transactions(transactions):
    n = len(transactions)
    for i in range(n):
        for j in range(n - i- 1):
            if float(transactions[j][2]) > float(transactions[j+1][2]):
                transactions[j], transactions[j+1] = transactions[j+1], transactions[j]
    return transactions

def search_transactions(transactions, amount):
    result = []
    for t in transactions:
        if float(t[2]) > amount:
            result.append(t)
    return result

def print_statement(transactions):
    print()
    print("Account\tType\tAmount\tDate")
    print("_"* 40)
    for t in transactions:
        print(f"{t[0]}\t{t[1]}\t{t[2]}\t{t[3]}")

