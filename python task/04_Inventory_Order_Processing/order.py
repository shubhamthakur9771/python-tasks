class Order:
    def __init__(self, customer_name):
        self.customer_name = customer_name
        self.products = []

    def add_product(self,product,quantity):
        self.products.append((product,quantity))

    def __str__(self):
        result = f"Customer: {self.customer_name}\n"
        for product, quantity in self.products:
            result += f"{product.name} x {quantity}\n"
        return result

    def undo_last_order(self):
        pass

    def pending_orders_to_be_shipped(self):
        pass

    def low_stock_alert(self):
        pass