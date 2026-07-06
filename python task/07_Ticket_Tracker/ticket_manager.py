from bug_ticket import BugTicket
from feature_ticket import FeatureTicket
import os

class TicketManager:
    def __init__(self):
        self.tickets = []

    def add_ticket(self,ticket):
        self.tickets.append(ticket)
        self.save_tickets()

    def update_status(self,ticket_id,new_status):
        for ticket in self.tickets:
            if ticket.ticket_id == ticket_id:
                ticket.status = new_status
                self.save_tickets()
                return True
        return False
    
    def close_ticket(self, ticket_id):
        for ticket in self.tickets:
            if ticket.ticket_id == ticket_id:
                ticket.status = "Done"
                self.save_tickets()
                return True
        return False
    
    def sort_by_priority(self):
        priority_rank = {
            "High" : 3,
            "Medium" : 2,
            "Low" : 1
        }
        n = len(self.tickets)
        for i in range(n-1):
            for j in range(n-i-1):
                first = priority_rank[self.tickets[j].priority]
                second = priority_rank[self.tickets[j+1].priority]
                if first < second:
                    self.tickets[j], self.tickets[j+1] = self.tickets[j+1], self.tickets[j]

    def save_tickets(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(base_dir,"tickets.txt")

        with open(filename,"w") as file:
            for ticket in self.tickets:
                if isinstance(ticket,BugTicket):
                    line = f"Bug,{ticket.ticket_id},{ticket.title},{ticket.priority},{ticket.status},{ticket.severity}\n"
                elif isinstance(ticket,FeatureTicket):
                    line = f"Feature,{ticket.ticket_id},{ticket.title},{ticket.priority},{ticket.status},{ticket.effort}\n"
                file.write(line)

    def load_tickets(self):
        self.tickets.clear()
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            filename = os.path.join(base_dir,"tickets.txt")
            with open(filename,"r") as file:
                for line in file:
                    data = line.strip().split(",")
                    if data[0] == "Bug":
                        ticket = BugTicket(int(data[1]),data[2],data[3],data[4],data[5])
                    elif data[0] == "Feature":
                        ticket = FeatureTicket(int(data[1]),data[2],data[3],data[4],data[5])
                    self.tickets.append(ticket)
        except FileNotFoundError:
            pass

    def display_kanban(self):
        print("\n ===== TO DO =====")
        for ticket in self.tickets:
            if ticket.status == "To Do":
                print(ticket.summary())
        
        print("\n ===== IN PROGRESS =====")
        for ticket in self.tickets:
            if ticket.status == "In Progress":
                print(ticket.summary())

        print("\n===== DONE =====")
        for ticket in self.tickets:
            if ticket.status == "Done":
                print(ticket.summary())

           
