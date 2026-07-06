from product import Product
from order import Order
import os

class Inventory:
    def __init__(self):
        self.products = []

    def load_stock(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(base_dir,"stock.txt")
        with open(filename,"r") as file:
            for line in file:
                data = line.strip().split(",")
                product = Product(data[0], data[1], data[2])
                self.products.append(product)

    def display_products(self):
        print("Available Products\n")
        for product in self.products:
            print(product)

    def find_product(self,name):
        for product in self.products:
            if product.name.lower() == name.lower():
                return product
    
        return None
    
    def place_order(self,undo_stack,shipping_queue):
        customer = input("Enter Customer Name: ")
        product_name = input("Enter Product Name: ")
        try:
            quantity = int(input("Enter Quantity: "))
        except ValueError:
            print("Invalid Quantity")
            return
            

        product = self.find_product(product_name)

        if product is None:
            print("Product not found")
            return

        if quantity > product.quantity:
            print("Insufficient Stock")
            return

        product.quantity -= quantity
        order = Order(customer)
        order.add_product(product,quantity)
        undo_stack.push(order)
        shipping_queue.enqueue(order)

        base_dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(base_dir,"orders.txt")

        with open(filename,"a") as file:
            total = product.price * quantity
            file.write(f"{customer},{product.name},{quantity},{total}\n")

        print("Order placed Successfully")

    
    def undo_last_order(self, undo_stack):
        if undo_stack.is_empty():
            print("No Orders to undo")
            return
        last_order = undo_stack.pop()
        for product , quantity in last_order.products:
            product.quantity += quantity
        print("Last order undone Successfully")


    def ship_order(self, shipping_queue):
        if shipping_queue.is_empty():
            print("No pending orders")
            return
        order = shipping_queue.dequeue()
        print(f"\n Order shipped for {order.customer_name}")
        print(order)

    def display_pending_orders(self,shipping_queue):
        shipping_queue.display()

    def low_stock_alert(self):
        print(f"\n Low Stock Products")

        found = False
        for product in self.products:
            if product.quantity < 5:
                print(product)
                found = True
        if not found:
            print("No low stock products")
    
    def merge_sort(self, arr):
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        left = self.merge_sort(arr[:mid])
        right = self.merge_sort(arr[mid:])
        return self.merge(left,right)
    
    def merge(self,left,right):
        result = []
        i = j= 0
        while i< len(left) and j < len(right):
            if left[i].price < right[j].price:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        result.extend(left[i:])
        result.extend(right[j:])
        return result
    
    def closest_products(self,budget):
        products = self.merge_sort(self.products)
        left = 0
        right = len(products) - 1
        best_pair = None
        smallest_diff = float("inf")
        while left < right:
            total = products[left].price + products[right].price
            diff = abs(budget - total)
            if diff < smallest_diff:
                smallest_diff = diff
                best_pair = (products[left], products[right], total)
            if total<budget:
                left+= 1
            else:
                right -= 1
        return best_pair
