class Contact:
    def __init__(self,name,phone,email,category):
        self.name = name
        self.phone = phone
        self.email = email
        self.category = category
    
    def __str__(self):
        return f"{self.name},{self.phone},{self.email},{self.category}"
    
    def display(self):
        print(f"Name: {self.name} | Phone : {self.phone} | Email : {self.email} | Category : {self.category}")

    

        