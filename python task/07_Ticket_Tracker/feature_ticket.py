from ticket import Ticket
class FeatureTicket(Ticket):
    def __init__(self, ticket_id, title, priority, status, effort):
        super().__init__(ticket_id, title, priority, status)
        self.effort = effort
    
    def summary(self):
        return f"{self.ticket_id} | {self.title} | {self.priority} | {self.status} | Effort : {self.effort}"