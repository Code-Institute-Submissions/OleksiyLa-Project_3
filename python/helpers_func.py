import os

ER = '\033[91m'
OK = '\033[92m'
Q = '\033[0m'


def clear_terminal():
    """
    Check the operating system and use the appropriate clear command
    """
    if os.name == 'posix':
        os.system('clear')
    elif os.name == 'nt':
        os.system('cls')


def log_exit_message(username):
    """
    This function prints a goodbye message
    """
    print("\nThank you for using the Calories Tracker App")
    if username is not None:
        print(f"\nGoodbye {username}\n")
    else:
        print("\nGoodbye\n")


def log(*message):
    """
    This function takes strings as arguments and prints them in a new line
    """
    message = "\n".join(message)
    print(message)


def confirm(msg):
    """
    This function asks for confirmation,
    if the input is not valid, it will ask for a new input
    """
    option = input(msg).lower()
    if option == "y" or option == "yes":
        return True
    elif option == "n" or option == "no":
        return False
    else:
        print(f"{ER}Wrong input, please type {Q}{OK}('y'/'yes') or ('n'/'no'){Q}")
        return confirm(msg)


def validate_length(data, input_message, min_length,
                    max_length, isSpaceProhibited=False):
    """
    This function checks if the input is between the min_length and max_length,
    if isSpaceProhibited is True, the input must not contain spaces
    If the input is not valid, the function will ask for a new input
    """
    if isSpaceProhibited:
        if len(data.split(" ")) > 1:
            print(f"{ER}rInput must not contain spaces{Q}")
            return validate_length(input(input_message), input_message,
                                   min_length, max_length, isSpaceProhibited)
    if len(data) < min_length:
        print(f"{ER}Input must be at least {min_length} characters long{Q}")
        return validate_length(input(input_message), input_message, min_length,
                               max_length, isSpaceProhibited)
    elif len(data) > max_length:
        print(f"{ER}Input must be less than {max_length} characters long{Q}")
        return validate_length(input(input_message), input_message, min_length,
                               max_length, isSpaceProhibited)
    else:
        return data


def is_number(data, input_message):
    """
    This function checks if the input is a number,
    if not, it will ask for a new input
    """
    try:
        int(data)
        return data
    except ValueError:
        print(f"{ER}Input must be an integer{Q}")
        return is_number(input(input_message), input_message)


def is_float(data, input_message):
    """
    This function checks if the input is a float or an integer,
    if not, it will ask for a new input
    """
    try:
        float_data = float(data)
        if str(int(float_data)) == data:
            return data
        else:
            return round(float_data, 1)
    except ValueError:
        print(f"{ER}Input must be a number{Q}")
        return is_float(input(input_message), input_message)
    

def validate_username(data, input_message):
    """
    This function checks if the username is valid,
    if not, it will ask for a new input
    """
    data = data.strip()
    if data == "":
        print(f"{ER}Username must not be empty{Q}")
        return validate_username(input(input_message), input_message)
    elif len(data.split(" ")) > 1:
        print(f"{ER}Username must not contain spaces{Q}")
        return validate_username(input(input_message), input_message)
    elif len(data) < 2:
        print(f"{ER}Username must be at least 2 characters long{Q}")
        return validate_username(input(input_message), input_message)
    elif len(data) > 20:
        print(f"{ER}Username must be less than 20 characters long{Q}")
        return validate_username(input(input_message), input_message)
    elif data[0].isdigit():
        print(f"{ER}Username must not start with a number{Q}")
        return validate_username(input(input_message), input_message)
    else:
        return data


def prepare_string(string):
    """
    This function takes a string and returns a string with the first
    letter of each word capitalized and the rest of the letters lowercase
    """
    return string.lower().title().strip()


def check_option(data, length):
    """
    This function checks if the input is between 1 and
    the length of the options, if not, it will ask for a new input
    """
    exit_num = length + 1
    option = int(data) - 1
    if option >= 0 and option < exit_num:
        return option
    else:
        print(f"{ER}Input must be between 1 and {exit_num}{Q}")
        return check_option(is_number(input("Select an option: "),
                                      "Select an option: "), length)


def select_option(*options):
    """
    This function takes functions as arguments
    and returns the selected function
    """
    print("\n")
    length = len(options)
    option = check_option(is_number(input("Select an option: "),
                                    "Select an option: "), length)
    if int(option) == length:
        return 'exit'
    clear_terminal()
    return options[option]


def enter_to_continue():
    """
    This function waits for the user to press enter
    """
    input(f"\nPress {OK}'Enter'{Q} to continue...")
    clear_terminal()


def wrapper_function(func, arg):
    """
    This function takes a function as an argument and returns
    a function that calls the function passed as an argument
    """
    def wrapper():
        func(arg)
    return wrapper
