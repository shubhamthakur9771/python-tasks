# from account import SavingsAccount, CurrentAccount
# from utils import read_transactions, sort_transactions, search_transactions

# print("===== BANK LEDGER SYSTEM =====")

# acc1 = SavingsAccount("SB101", 10000, 5)

# acc2 = CurrentAccount("CA201", 5000, 3000)

# try:

#     acc1.deposit(2000)

#     acc1.withdraw(1000)

#     acc2.deposit(3000)

#     acc2.withdraw(7000)

#     acc1.show_balance()

#     acc2.show_balance()

# except Exception as e:

#     print(e)

# print("\nApplying Monthly Updates\n")

# accounts = [acc1, acc2]

# for account in accounts:

#     account.apply_monthly_update()

# print("\nUpdated Balances")

# acc1.show_balance()

# acc2.show_balance()

# print("\nReading Transaction Statement")

# transactions = read_transactions()

# print()

# for t in transactions:
#     print(t)

# print("\nSorted By Amount")

# sorted_transactions = sort_transactions(transactions)

# for t in sorted_transactions:
#     print(t)

# print("\nTransactions Above 2500")

# result = search_transactions(transactions, 2500)

# for t in result:
#     print(t)

from account import SavingsAccount, CurrentAccount
from utils import (
    read_transactions,
    sort_transactions,
    search_transactions,
    print_statement
)

# Create accounts
accounts = {
    "SB101": SavingsAccount("SB101", 10000, 5),
    "CA201": CurrentAccount("CA201", 5000, 3000)
}


def get_account():
    account_no = input("Enter Account Number: ").strip()

    if account_no not in accounts:
        print("Account does not exist.")
        return None

    return accounts[account_no]


while True:

    print("\n========== BANK LEDGER ==========")
    print("1. Deposit")
    print("2. Withdraw")
    print("3. Show Balance")
    print("4. Apply Monthly Update")
    print("5. View Transaction Statement")
    print("6. Sort Transactions by Amount")
    print("7. Search Transactions Above Amount")
    print("8. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":

        account = get_account()

        if account:
            try:
                amount = float(input("Enter deposit amount: "))
                account.deposit(amount)
                print("Deposit Successful")

            except Exception as e:
                print(e)

    elif choice == "2":

        account = get_account()

        if account:
            try:
                amount = float(input("Enter withdrawal amount: "))
                account.withdraw(amount)
                print("Withdrawal Successful")

            except Exception as e:
                print(e)

    elif choice == "3":

        account = get_account()

        if account:
            account.show_balance()

    elif choice == "4":

        print("\nApplying Monthly Updates...\n")

        for account in accounts.values():
            account.apply_monthly_update()

        print("Monthly Update Completed")

    elif choice == "5":

        transactions = read_transactions()

        if transactions:
            print_statement(transactions)

    elif choice == "6":

        transactions = read_transactions()

        if transactions:
            sorted_transactions = sort_transactions(transactions)
            print_statement(sorted_transactions)

    elif choice == "7":

        transactions = read_transactions()

        if transactions:
            amount = float(input("Enter minimum amount: "))

            result = search_transactions(transactions, amount)

            if result:
                print_statement(result)
            else:
                print("No transactions found.")

    elif choice == "8":

        print("Thank you for using Bank Ledger.")
        break

    else:

        print("Invalid choice. Please try again.")