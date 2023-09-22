from googlesheet import googleSheetDB, authGS, productListGS
from helpers_func import clear_terminal, log_exit_message, log, confirm, validate_length, is_number, prepare_string, select_option
from options import login, register, add_new_product, read_product, update_product, delete_product, calculate_calories, set_calories_limit, update_password, delete_account, add_consumed_calories, get_consumed_calories, calculate_calories_limit, calculate_overall_progress, add_your_weight


def auth():
    """
    This function is the menu of the authentication, it will be displayed when the app starts
    When the user logs in or register, the menu function will be displayed
    """
    while True:
        log("Type '1' to login, '2' to register or '3' to exit", "Please select an option:", "1. Login", "2. Register", "3. Exit")
        option = select_option(login, register)
        if option == 'exit':
            print("Goodbye")
            break
        clear_terminal()
        return option()


def crud():
    """
    This function is the menu of the CRUD operations
    """
    clear_terminal()
    while True:
        log("1. Create a new product", "2. Read a product", "3. Update a product", "4. Delete a product", "5. Go Back")
        option = select_option(add_new_product, read_product, update_product, delete_product)
        if option == 'exit':
            clear_terminal()
            break
        option()


def manage_personal_info():
    """
    This function is the menu of the personal info
    """
    clear_terminal()
    while True:
        log("1. Change password", "2. Delete account", "3. Add calories consumed per today", "4. Set calories limit", "5. See calories consumed per today", "6. See calories limit", "7. See your progress", "8. Add your weight", "9. Go Back")
        option = select_option(update_password, delete_account, add_consumed_calories, set_calories_limit, get_consumed_calories, calculate_calories_limit, calculate_overall_progress, add_your_weight)
        if option == 'exit':
            clear_terminal()
            break
        option()


def menu():
    """
    This function is the main menu of the app, it will be displayed after the user logs in
    """
    while True:
        if authGS.username is None:
            log_exit_message(authGS.username)
            return
        log("1. CRUD calories table", "2. Calculate calories", "3. Personal info", "4. Exit")
        option = select_option(crud, calculate_calories, manage_personal_info)
        if option == 'exit':
            clear_terminal()
            log_exit_message(authGS.username)
            break
        option()


def main():
    """
    Start the Calories Tracker App
    """
    clear_terminal()
    print("Welcome to the Calories Tracker App")
    if auth():
        menu()


main()