import re as _re
from constants import (
                        MATRIC_NUMBER_PATTERN,
                        PHONE_NUMBER_PATTERN
                    )


class Validator:
    def validate_username(self, username: str) -> tuple:
        
        error_message = None

        if not username:
            error_message = "Username field required to proceed"
            return (False, error_message)

        username = username.strip()

        if not 4 < len(username) < 16:
            error_message = "A valid username must contain a minimum of 5 and a maximum of 15 characters"

        elif username.isspace():
            error_message = "Username must not contain any space"

        elif not username.isalnum():
            error_message = "Username can only consist of alphabets and numbers"

        if error_message:
            return (False, error_message)

        __cleaned_username = username.lower()

        return (True, __cleaned_username)

    def validate_fullname(self, full_name: str) -> tuple:
        error_message = None
        if not full_name:
            error_message = "Name field required to proceed"
            return (False, error_message)

        full_name = full_name.strip().split()

        if len(full_name) != 2:
            error_message = "Only first name and last name are required (A total of two names)\nDid you mistakenly put a space inbetween a name?"
      
        elif [True for name in full_name if not name.isalpha()]:
            error_message = "Names must contain only alphabets"

        elif [True for name in full_name if not 2 < len(name) < 15]:
            error_message = "A valid name should be a minimum of 3 and a maximum of 15 characters"

        if error_message:
            return (False, error_message)

        cleaned_name = " ".join(full_name).title().strip()

        return (True, cleaned_name)        

    def validate_name(self, name: str) -> tuple:
        error_message = None
        if not name:
            error_message = "Name field required to proceed"
            return (False, error_message)

        if not 2 < len(name) < 15:
            error_message = "A valid name should be a minimum of 3 and a maximum of 15 characters"

        elif not name.isalpha():
            error_message = "Names must contain only alphabets"

        if error_message:
            return (False, error_message)
        
        cleaned_name = name.title().strip()
        return (True, cleaned_name) 

    def validate_name_or_full_name(self, name: str) -> tuple:
        error_message = None
        if len(name.split()) > 1:
            name_valid, error_or_cleaned_name = self.validate_fullname(name)
            if name_valid:
                cleaned_name = error_or_cleaned_name
            else:
                error_message = error_or_cleaned_name
        else:
            name_valid, error_or_cleaned_name = self.validate_name(name)
            if name_valid:
                cleaned_name = error_or_cleaned_name
            else:
                error_message = error_or_cleaned_name  

        if error_message:
            return (False, error_message)

        return (True, cleaned_name)

    def validate_phone_number(self, phone_number: str) -> tuple:
        error_message = None

        if phone_number == "" or phone_number is None:
            error_message = "Phone number field required to proceed"
            return (False, error_message)

        pattern = _re.compile(PHONE_NUMBER_PATTERN)

        if not _re.match(pattern, phone_number):
            error_message = 'Phone number should be in this format "09025438896", (All numeric)'

        if error_message:
            return (False, error_message)
        return (True, phone_number)

    def validate_password(self, username=None, password=None, _password=None) -> tuple:
        error_message = None

        if not password:
            error_message = "Password field require to proceed"
            return (False, error_message)

        if not 8 < len(password) < 15:
            error_message = "Passwords must be a minimum of 8 and a maximum of 15"
        elif password.isnumeric():
            error_message = "Password too weak, (contains only numbers) please enter a stronger password"
        elif password.isalpha():
            error_message = "Password too weak, (contains only alphabets) please enter a stronger password"
        elif username.lower() in password.lower():
            error_message = "Password too similar to username, kindly create a combination not involving username"

        if error_message:
            return (False, error_message)

        _cleaned_password = password.strip()
        return (True, _cleaned_password)

    def validate_login(self, username=None, password=None) -> tuple:
        error_message = None

        if not(username and password):
            error_message = "Username and password required"

        if error_message:
            return (False, error_message)

        return (True, None)

    def validate_matric_number(self, matric_number: str) -> bool:
        # Matric number pattern can be compiled to match a new pattern as required
        matric_number = matric_number.upper().strip()
        if _re.match(_re.compile(MATRIC_NUMBER_PATTERN), matric_number):
            return True
        return False
