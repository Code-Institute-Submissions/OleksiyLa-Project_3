from python.googlesheet import authGS
import python.helpers_func as helpers
import python.options as options


def auth():
    """
    This function is the menu of the authentication,
    it will be displayed when the app starts
    When the user logs in or register, the menu function will be displayed
    """
    while True:
        helpers.log("Select an option:", "1. Login", "2. Register", "3. Exit")
        option = helpers.select_option(options.login, options.register)
        if option == 'exit':
            print("Goodbye")
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
    helpers.clear_terminal()
    while True:
        helpers.log("1. Create a new product", "2. Read a product",
                    "3. Update a product", "4. Delete a product", "5. Go Back")
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
    helpers.clear_terminal()
    while True:
        helpers.log("1. Set your calories limit", "2. Set your weight",
                    "3. Add calories consumed per today", "4. Go Back")
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
    helpers.clear_terminal()
    while True:
        helpers.log("1. Get your calories limit",
                    "2. Get your calories consumed so far today", "3. Go Back")
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
        helpers.log("1. Product table",
                    "2. Enter product to calculate calories",
                    "3. Get your personal data",
                    "4. Set your personal data",
                    "5. See your progress",
                    "6. Your account",
                    "7. Exit")
        option = helpers.select_option(crud,
                                       options.calculate_calories,
                                       get_your_personal_data,
                                       set_your_personal_data,
                                       options.see_progress,
                                       options.manage_account)
        if option == 'exit':
            helpers.clear_terminal()
            conf_text = "Are you sure you want to exit? (y/n) or (yes/no): "
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
    print("Welcome to the Calories Tracker App")
    if auth():
        menu()


main()
