import re
class Validator:
    @staticmethod
    def validate_phone(phone):
        if not phone.isdigit():
            return False, "Phone contains Non-digit characters"
        if len(phone) != 10:
            return False, "Phone should contain exactly 10 digits"
        return True, ""
    
    @staticmethod
    def validate_email(email):
        pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
        if re.match(pattern,email):
            return True, ""
        return False, "Invalid Email Format"
