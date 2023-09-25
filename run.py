from python.googlesheet import authGS
import python.helpers_func as helpers
import python.options as options

OK = '\033[92m'
Q = '\033[0m'


def auth():
    """
    This function is the menu of the authentication,
    it will be displayed when the app starts
    When the user logs in or register, the menu function will be displayed
    """
    while True:
        print(f" Please, {OK}login{Q} or {OK}register{Q}\n ")
        helpers.log(" 1. Login", " 2. Register", " 3. Exit")
        option = helpers.select_option(options.login, options.register)
        if option == 'exit':
            print(" Goodbye")
            exit()
        helpers.clear_terminal()
        if option():
            return True
        else:
            continue


def crud():
    """
    This function is the menu of the CRUD operations
    """
    while True:
        helpers.clear_terminal()
        print(f"\n {OK}Manage calories table{Q}\n ")
        helpers.log(" 1. Create a new product", " 2. Read a product",
                    " 3. Update a product", " 4. Delete a product", "5. Go Back")
        option = helpers.select_option(options.add_new_product,
                                       options.read_product,
                                       options.update_product,
                                       options.delete_product)
        if option == 'exit':
            helpers.clear_terminal()
            break
        option()


def set_your_personal_data():
    """
    This function is the menu that allows the user to set his personal data
    """
    while True:
        helpers.clear_terminal()
        print(f"\n {OK}Set your personal data{Q}\n ")
        helpers.log(" 1. Set your calories limit", " 2. Set your weight",
                    " 3. Add calories consumed per today", " 4. Go Back")
        option = helpers.select_option(options.set_calories_limit,
                                       options.add_your_weight,
                                       options.add_consumed_calories)
        if option == 'exit':
            helpers.clear_terminal()
            break
        option()


def get_your_personal_data():
    """
    This function is the menu that allows the user to get his personal data
    """
    while True:
        helpers.clear_terminal()
        print(f"\n {OK}Get your personal data{Q}\n ")
        helpers.log(" 1. Get your calories limit",
                    " 2. Get your calories consumed so far today", "3. Go Back")
        option = helpers.select_option(options.calculate_calories_limit,
                                       options.get_consumed_calories)
        if option == 'exit':
            helpers.clear_terminal()
            break
        option()


def menu():
    """
    This function is the main menu of the app,
    it will be displayed after the user logs in
    """
    while True:
        print(f"\n {OK}Main menu{Q}\n ")
        helpers.log(" 1. Product table",
                    " 2. Enter product to calculate calories",
                    " 3. Get your personal data",
                    " 4. Set your personal data",
                    " 5. See your progress",
                    " 6. Your account",
                    " 7. Exit")
        option = helpers.select_option(crud,
                                       options.calculate_calories,
                                       get_your_personal_data,
                                       set_your_personal_data,
                                       options.see_progress,
                                       options.manage_account)
        if option == 'exit':
            helpers.clear_terminal()
            conf_text = "\n Are you sure you want to exit? "
            conf_text += f"{OK}(y/n) or (yes/no):{Q} "
            if helpers.confirm(conf_text):
                helpers.clear_terminal()
                helpers.log_exit_message(authGS.username)
                exit()
            else:
                helpers.clear_terminal()
                continue
        option()


def main():
    """
    Start the Calories Tracker App
    """
    helpers.clear_terminal()
    print(f"{OK}\n Welcome to the Calories Tracker App{Q}\n ")
    if auth():
        menu()


main()
