import re


def validate_email(email: str) -> bool:
    
    if re.match(r'^[\w\.]+@[a-zA-Z1-9]+\.[a-zA-Z]{3}$',email):
        print(True)
            
    else :
        print(False)

def validate_phone(number: str) -> bool:
    n=len(number)
    if n == 11:
        if re.match(r'^09[\d]{9}$',number):
            print(True)
        else :
            print(False)
        
    elif n == 13:
        if re.match(r'^\+989[\d]{9}$',number):
            print(True)
        else :
            print(False)        
    
    elif n == 14:
        if re.match(r'^00989[\d]{9}$',number):
            print(True)
        else :
            print(False)     