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
    """
    This function prints a goodbye message
    """
    print("Thank you for using the Calories Tracker App")
    if username is not None:
        print(f"Goodbye {username}")
    else:
        print("Goodbye")


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
        print("Wrong input, please type ('y'/'yes') or ('n'/'no')")
        confirm(msg)


def validate_length(data, input_message, min_length,
                    max_length, isSpaceProhibited=False):
    """
    This function checks if the input is between the min_length and max_length,
    if isSpaceProhibited is True, the input must not contain spaces
    If the input is not valid, the function will ask for a new input
    """
    if isSpaceProhibited:
        if len(data.split(" ")) > 1:
            print("Input must not contain spaces")
            return validate_length(input(input_message), input_message,
                                   min_length, max_length, isSpaceProhibited)
    if len(data) < min_length:
        print(f"Input must be at least {min_length} characters long")
        return validate_length(input(input_message), input_message, min_length,
                               max_length, isSpaceProhibited)
    elif len(data) > max_length:
        print(f"Input must be less than {max_length} characters long")
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
        print("Input must be an integer")
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
        print("Input must be a number")
        return is_float(input(input_message), input_message)


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
        print(f"Input must be between 1 and {exit_num}")
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
    input("\nPress 'Enter' to continue...")
    clear_terminal()


def wrapper_function(func, arg):
    """
    This function takes a function as an argument and returns
    a function that calls the function passed as an argument
    """
    def wrapper():
        func(arg)
    return wrapper
