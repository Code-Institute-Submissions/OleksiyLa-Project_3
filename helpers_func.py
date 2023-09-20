import os

def clear_terminal():
    """
      Check the operating system and use the appropriate clear command
    """
    if os.name == 'posix':
        os.system('clear')
    elif os.name == 'nt':
        os.system('cls')

def log_exit_message(username):
    print("Thank you for using the Calories Tracker App")
    if username is not None:
        print(f"Goodbye {username}")
    else:
        print("Goodbye")

def log(*message):
    message = "\n".join(message)
    print(message)

def confirm(msg):
    option = input(msg).lower()
    if option == "y" or option == "yes":
        return True
    elif option == "n" or option == "no":
        return False
    else:
        print("Wrong input, please type 'y' or 'n'")
        confirm(msg)

def validate_length(data, input_message, min_length, max_length, isSpaceProhibited = False):
    if isSpaceProhibited:
        if len(data.split(" ")) > 1:
            print("Input must not contain spaces")
            return validate_length(input(input_message), input_message, min_length, max_length, True)
    if len(data) < min_length:
        print(f"Input must be at least {min_length} characters long")
        return validate_length(input(input_message), input_message, min_length, max_length, True)
    elif len(data) > max_length:
        print(f"Input must be less than {max_length} characters long")
        return validate_length(input(input_message), input_message, min_length, max_length, True)
    else:
        return data
    
def is_number(data, input_message):
    try:
        int(data)
        return data
    except ValueError:
        print("Input must be a number")
        return is_number(input(input_message), input_message)
    
def prepare_string(string):
    return string.lower().title().strip()

def check_option(data, length):
    # try:
    exit_num = length + 1
    option = int(data) - 1
    if option >= 0 and option < exit_num:
        return option
    else:
        print(f"Input must be between 1 and {exit_num}")
        return check_option(is_number(input("Select an option: "), "Select an option: "), length)
    # except ValueError:
    #     return check_option(is_number(input("Select an option: ")), length)

def select_option(*options):
    print("\n")
    length = len(options)
    option = check_option(is_number(input("Select an option: "), "Select an option: "), length)
    if int(option) == length:
        return 'exit'
    return options[option]