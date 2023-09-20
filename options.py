from googlesheet import googleSheetDB, authGS, productListGS
from helpers_func import clear_terminal, log_exit_message, log, confirm, validate_length, is_number, prepare_string, select_option

def login():
    print("Login:")
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    if authGS.login(username, password):
        clear_terminal()
        print(f"Welcome {username}")
        return True
    else:
        print("Invalid username or password")
        return False
    
def register():
    print("Register:")
    username = validate_length(input("Enter your username: "), "Enter your username: ", 2, 12, True)
    password = validate_length(input("Enter your password: "), "Enter your password: ", 6, 12, True)
    if authGS.register(username, password):
        clear_terminal()
        log("Registration successful", f"Welcome {username}")
        return True
    else:
        print("Username already exists")
        return False