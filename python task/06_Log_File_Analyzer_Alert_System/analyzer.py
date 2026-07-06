from log_entry import LogEntry
import os
class LogAnalyzer:
    def __init__(self):
        self.logs = []
        self.invalid_lines = []

    def load_logs(self,filename_i):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(base_dir,filename_i)
        with open(filename,"r") as file:
            for line in file:
                data = line.strip().split(" | ")
                if len(data) != 3:
                    self.invalid_lines.append(line.strip())
                    continue
                timestamp = data[0]
                level = data[1]
                message = data[2]
                log = LogEntry(timestamp,level,message)
                self.logs.append(log)

    def show_invalid(self):
        print("Malformed Lines")
        for line in self.invalid_lines:
            print(line)
    
    def level_frequency(self):
        frequency = {}
        for log in self.logs:
            if log.level in frequency:
                frequency[log.level] += 1
            else:
                frequency[log.level] = 1
        return frequency
    
    def get_error_logs(self):
        errors = []
        for log in self.logs:
            if log.level == "ERROR":
                errors.append(log)
        return errors
    
    def write_errors(self,filename_i):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(base_dir,filename_i)
        errors = self.get_error_logs()
        with open(filename,"w") as file:
            for log in errors:
                file.write(str(log) + "\n")

    def error_alert(self):
        window_size = 5
        for i in range(len(self.logs) - window_size +1):
            error_count = 0
            for j in range(i,i+window_size):
                if self.logs[j].level == "ERROR":
                    error_count += 1
            if error_count >= 3:
                print("ALERT!")
                print(f"Window {i+1} to window {i + window_size}")
                for j in range(i, i +window_size):
                    print(self.logs[j])
                print()

    def most_common_error(self):
        frequency = {}
        for log in self.logs:
            if log.level == "ERROR":
                if log.message in frequency:
                    frequency[log.message] += 1
                else:
                    frequency[log.message] = 1
        max_count = 0
        max_message = ""

        for message in frequency:
            if frequency[message] > max_count:
                max_count = frequency[message]
                max_message = message
        print("Most Frequent Error")
        print(max_message)
        print(f"Occurred: {max_count} times")




    
                

