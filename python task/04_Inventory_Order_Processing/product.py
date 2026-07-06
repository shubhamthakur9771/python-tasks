class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = float(price)
        self.quantity = int(quantity)

    def __str__(self):
        return f"{self.name} | Price : ₹{self.price} | Stock : {self.quantity}"