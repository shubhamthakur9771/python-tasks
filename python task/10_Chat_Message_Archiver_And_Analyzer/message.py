class Message:
    def __init__(self, sender,timestamp,text):
        self.sender = sender
        self.timestamp = timestamp
        self.text = text
    
    def __str__(self):
        return f"{self.sender} | {self.timestamp} | {self.text}"
    
    

    