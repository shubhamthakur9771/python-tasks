from contact import Contact
from validator import Validator
from logger import Logger
import os

class ContactManager:
    def __init__(self):
        self.contacts = []
    
    def add_contact(self,contact):
        valid_phone, msg = Validator.validate_phone(contact.phone)
        if not valid_phone:
            print(msg)
            return
        valid_email, message = Validator.validate_email(contact.email)
        if not valid_email:
            print(message)
            return
        self.contacts.append(contact)

    def save_contacts(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(base_dir,"contacts.txt")
        with open(filename,"w") as file:
            for contact in self.contacts:
                file.write(str(contact) + "\n")

    def load_contacts(self):
        self.contacts.clear()
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            filename = os.path.join(base_dir,"contacts.txt")
            with open(filename,"r") as file:
                for line in file:
                    data = line.strip().split(",")
                    if len(data) != 4:
                        Logger.log(f"{line.strip()} -> invalid number of fields")
                        continue
                    name, phone, email, category = data
                    valid_phone, message = Validator.validate_phone(phone)
                    if not valid_phone:
                        Logger.log(f"{line.strip()} -> {message}")
                        continue
                    valid_email, msg = Validator.validate_email(email)
                    if not valid_email:
                        Logger.log(f"{line.strip()} -> {msg}")
                        continue
                    self.contacts.append(Contact(name,phone,email,category))
        except FileNotFoundError:
            print("contacts.txt not found")
        
    def display_contacts(self):
        if not self.contacts:
            print("No Contact")
            return
        for contact in self.contacts:
            contact.display()
            print("-"*20)

    def search_contact(self,name):
        for contact in self.contacts:
            if contact.name.lower() == name.lower():
                return contact
        return None
    
    def sort_contacts(self):
        self.contacts.sort(key=lambda c:c.name.lower())

    def binary_search(self,name):
        self.sort_contacts()
        low =0
        high = len(self.contacts) - 1
        while low <= high:
            mid = (low + high)//2
            current = self.contacts[mid].name.lower()

            if current == name.lower():
                return self.contacts[mid]
            elif current < name.lower():
                low = mid +1
            else:
                high = mid - 1
        return None
    
    def find_duplicates(self):
        phone_dict = {}
        duplicates = []
        for contact in self.contacts:
            if contact.phone in phone_dict:
                if phone_dict[contact.phone] != contact.name:
                    duplicates.append((phone_dict[contact.phone], contact.name,contact.phone))
            else:
                phone_dict[contact.phone] = contact.name
        return duplicates




    



