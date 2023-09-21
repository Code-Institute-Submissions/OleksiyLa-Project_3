from googlesheet import googleSheetDB, authGS, productListGS
from helpers_func import clear_terminal, log_exit_message, log, confirm, validate_length, is_number, prepare_string, select_option
from options import login, register, add_new_product, read_product, update_product, delete_product, calculate_calories, set_calories_limit, update_password, delete_account

def auth():
    while True:
        log("Type '1' to login, '2' to register or '3' to exit", "Please select an option:", "1. Login", "2. Register", "3. Exit")
        option = select_option(login, register)
        if option == 'exit':
            print("Goodbye")
            break
        clear_terminal()
        return option()

def crud():
    while True:
        log("1. Create a new product", "2. Read a product", "3. Update a product", "4. Delete a product", "5. Go Back")
        option = select_option(add_new_product, read_product, update_product, delete_product)
        if option == 'exit':
            clear_terminal()
            break
        return option()

def manage_personal_info():
    while True:
        log("1. Change password", "2. Delete account", "3. Add calories consumed per today", "4. Set calories limit", "5. See calories consumed per today", "6. See calories limit", "7. See your progress", "8. Add your weight", "9. Go Back")
        option = input("Enter your option: ")
        if option == "1":
            update_password()
        elif option == "2":
            if delete_account():
                break
        elif option == "3":
            calories_consumed = input("Enter how many calories you have consumed this day: ")
            googleSheetDB.add_calories_consumed(calories_consumed)
        elif option == "4":
            set_calories_limit()
        elif option == "5":
            print("You've consumed " + googleSheetDB.get_calories_consumed() + " calories today")
        elif option == "6":
            print("Your calories limit per day is " + googleSheetDB.get_calories_limit())
        elif option == "7":
            print(googleSheetDB.calculate_overall_progress())
        elif option == "8":
            googleSheetDB.add_weight(input("Enter your weight: "))
        elif option == "9":
            clear_terminal()
            break
        else:
            print("Invalid option, please type 1,")

def menu():
    while True:
        if authGS.username is None:
            log_exit_message(authGS.username)
            return
        log("1. CRUD calories table", "2. Calculate calories", "3. Personal info", "4. Exit")
        option = input("Enter your option: ")
        if option == "1":
            clear_terminal()
            crud()
        elif option == "2":
            clear_terminal()
            calculate_calories()
        elif option == "3":
            clear_terminal()
            manage_personal_info()
        elif option == "4":
            clear_terminal()
            log_exit_message(authGS.username)
            break
        else:
            print("Invalid option, please type 1, 2 or 3")

def main():
    """
    Start the Calories Tracker App
    """
    clear_terminal()
    print("Welcome to the Calories Tracker App")
    if auth():
        menu()

main()