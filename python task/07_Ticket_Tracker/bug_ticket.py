from ticket import Ticket

class BugTicket(Ticket):
    def __init__(self, ticket_id, title, priority, status, severity):
        super().__init__(ticket_id, title, priority, status)
        self.severity = severity
    
    def summary(self):
        return f"{self.ticket_id} | {self.title} | {self.priority} | {self.status} | Severity : {self.severity}"