class Ticket:
    def __init__(self,ticket_id,title,priority,status):
        self.ticket_id = ticket_id
        self.title = title
        self.priority = priority
        self.status =status
    
    def summary(self):
        return f"{self.ticket_id} | {self.title} | {self.priority} | {self.status}"
    