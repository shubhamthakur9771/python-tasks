from transaction import Transaction
from exceptions import InvalidAmountError, InsufficientFundsError

class Account:
    def __init__(self, account_no, balance):
        self.account_no = account_no
        self.__balance = balance
    def get_balance(self):
        return self.__balance
    
    def deposit(self, amount):

        if amount <= 0:
            raise InvalidAmountError("Amount must be positive.")
        self.__balance += amount
        self.log_transaction("Deposit",amount)

    def withdraw(self, amount):
        if amount <= 0:
            raise InvalidAmountError("Amount must be positive")
        
        if amount > self.get_balance():
            raise InsufficientFundsError("Insufficient Balance.")
        
        self.__balance -= amount
        self.logtransaction("Withdraw",amount)

    def show_balance(self):
        print(f"Balance : {self.get_balance()}")

    def log_transaction(self,transaction_type, amount):
        t = Transaction(self.account_no ,transaction_type,amount)
        with open("transactions.txt", "a") as file:
            file.write(str(t) + "\n")

    def apply_monthly_update(self):
        print(f"No monthly update for Account {self.account_no}")


class SavingsAccount(Account):
    def __init__(self, account_no, balance, interest_rate):
        super().__init__(account_no, balance)
        self.interest_rate = interest_rate
    
    def apply_interest(self):
        interest = self.get_balance() * self.interest_rate/100
        self.deposit(interest)

    def apply_monthly_update(self):
        print(f"Applying interest to {self.account_no}")
        self.apply_interest()

class CurrentAccount(Account):
    def __init__(self, account_no, balance, overdraft_limit):
        super().__init__(account_no, balance)
        self.overdraft_limit = overdraft_limit
    
    def withdraw(self, amount):
        
        if amount <= 0:
            raise InvalidAmountError("Amount must be positive")
        
        available = self.get_balance() + self.overdraft_limit
        
        if amount > available:
            raise InsufficientFundsError("Overdraft Limit Exceeded")
        balance = self.get_balance()
        new_balance = balance - amount
        self._Account__balance = new_balance
        self.log_transaction("Withdraw", amount)

    def apply_monthly_update(self):
        print(f"Current Account {self.account_no} monthly update")