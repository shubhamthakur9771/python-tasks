from datetime import datetime

class Transaction:
    def __init__(self, account_no, transaction_type, amount):
        self.account_no = account_no
        self.transaction_type = transaction_type
        self.amount = amount
        self.time = datetime.now()

    def __str__(self):
        return f"{self.account_no},{self.transaction_type},{self.amount},{self.time}"