import os
from message import Message
from datetime import datetime
class ChatAnalyzer:
    def __init__(self):
        self.messages = []
        self.invalid_lines = []

    def load_messages(self, filename_i):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(base_dir,filename_i)
        with open(filename,"r") as file:
            for line in file:
                data = line.strip().split(" | ")
                if(len(data) != 3):
                    self.invalid_lines.append(line.strip())
                    continue
                message = Message(data[0], data[1],data[2])
                self.messages.append(message)

    def write_errors(self, filename_i):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(base_dir,filename_i)
        with open(filename,"w") as file:
            for line in self.invalid_lines:
                file.write(line + "\n")

    def sort_messages(self):
        for i in range(1, len(self.messages)):
            current = self.messages[i]
            j = i-1
            while(j >= 0 and self.messages[j].timestamp> current.timestamp):
                self.messages[j+1] = self.messages[j]
                j -= 1
            self.messages[j+1] = current

    def export_chat(self,filename_i):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(base_dir,filename_i)
        with open(filename,"w") as file:
            for message in self.messages:
                file.write(str(message) + "\n")

    def word_frequency(self):
        sender_words = {}
        for message in self.messages:
            sender = message.sender
            if sender not in sender_words:
                sender_words[sender] = {}
            words = message.text.lower().split()
            for word in words :
                word = word.strip(".,!?;:\"'()[]{}")
                if word == "":
                    continue
                if word in sender_words[sender]:
                    sender_words[sender][word] += 1

                else:
                    sender_words[sender][word] = 1
        return sender_words
    
    def top_five_words(self):
        sender_words = self.word_frequency()
        for sender in sender_words:
            print("\nSender: ", sender)
            temp = sender_words[sender].copy()
            count = 0
            while count < 5 and len(temp) > 0:
                max_word = ""
                max_freq  = -1
                for word in temp:
                    if temp[word] > max_freq:
                        max_freq = temp[word]
                        max_word = word

                print(f"{max_word} : {max_freq}")
                del temp[max_word]
                count += 1

    def longest_silence(self):
        if len(self.messages) < 2:
            print("Not enough messages")
            return
        max_gap = 0
        start_msg = None
        end_msg = None
        for i in range(1,len(self.messages)):
            t1 = datetime.strptime(self.messages[i-1].timestamp, "%Y-%m-%d %H:%M:%S")
            t2 = datetime.strptime(self.messages[i].timestamp,"%Y-%m-%d %H:%M:%S")
            gap = (t2-t1).total_seconds()
            if gap > max_gap:
                max_gap = gap
                start_msg = self.messages[i-1]
                end_msg = self.messages[i]
        print("Longest Silence Gap")
        print("--------------------")
        print(f"Gap : {max_gap} seconds")
        print("From: ")
        print(start_msg)
        print("To")
        print(end_msg)







