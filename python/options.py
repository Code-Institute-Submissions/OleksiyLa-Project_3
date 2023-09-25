from python.googlesheet import googleSheetDB, authGS, productListGS
import python.helpers_func as helpers

ER = '\033[91m'
OK = '\033[92m'
Q = '\033[0m'


# Authentication functions
def login():
    """
    This function logs in the user to the google sheet
    """
    print(f"\n{OK}Login:{Q}")
    username = helpers.validate_username(input("\nEnter your username: "),
                                         "\nEnter your username: ")
    password = helpers.validate_length(input("\nEnter your password: "),
                                       "\nEnter your password: ", 6, 12, True)
    if authGS.login(username, password):
        helpers.clear_terminal()
        print(f"\n{OK}Welcome {username}{Q}")
        return True
    else:
        helpers.clear_terminal()
        print(f"{ER}Invalid username or password{Q}")
        return False


def register():
    """
    This function registers a new user to the google sheet,
    if the username already exists, it will not be added
    """
    print(f"\n{OK}Register:{Q}")
    username = helpers.validate_username(input("\nEnter your username: "),
                                         "\nEnter your username: ")
    password = helpers.validate_length(input("\nEnter your password: "),
                                       "\nEnter your password: ", 6, 12, True)
    if authGS.register(username, password):
        helpers.clear_terminal()
        helpers.log(f"\n{OK}Registration successful{Q}\n",
                    f"{OK}Welcome {username}{Q}\n")
        return True
    else:
        helpers.clear_terminal()
        print(f"{ER}\nUsername '{username}' already exists, try again{Q}\n")
        return register()


# Product table functions (CRUD)
def add_new_product():
    """
    This function adds a new product to the google sheet,
    if the product already exists, it will not be added
    """
    print(f"\n{OK}Add new product:{Q}\n")
    valid_product = helpers.prepare_string(
        helpers.validate_length(input("Enter the product: "),
                                "Enter the product: ", 1, 20))
    if productListGS.find_product(valid_product):
        print(f"{ER}Product {valid_product} already exists{Q}")
        helpers.enter_to_continue()
        return
    conf_text = f"Are you sure you want to add a new product '{valid_product}'"
    if not helpers.confirm(conf_text + f"? {OK}(y/n) or (yes/no):{Q} "):
        return
    valid_calories = helpers.is_number(input("Enter the calories: "),
                                       "Enter the calories: ")
    valid_calories = abs(int(valid_calories))
    isProductAdded = productListGS.add_product(valid_product,
                                               valid_calories)
    if isProductAdded:
        print(f"{OK}Product added successfully{Q}")
    else:
        print(f"{ER}Error adding product{Q}")
    helpers.enter_to_continue()


def read_product():
    """
    This function reads a product from the google sheet
    """
    print(f"\n{OK}Read product:{Q}\n")
    valid_products = helpers.prepare_string(helpers.validate_length(
        input("Enter the product name: "),
        "Enter the product name: ", 1, 20))
    products = productListGS.find_products_starting_with(valid_products)
    helpers.clear_terminal()
    for product in products:
        print(product[0] + ": " + product[1] + " calories")
    if len(products) == 0:
        print(f"{ER}Product '{valid_products}' not found{Q}")
        conf_txt = f"Would you like to add '{valid_products}' to the database?"
        if helpers.confirm(conf_txt + f" {OK}(y/n) or (yes/no):{Q} "):
            valid_calories = helpers.is_number(input("Enter the calories: "),
                                               "Enter the calories: ")
            valid_calories = abs(int(valid_calories))
            isProductAdded = productListGS.add_product(valid_products,
                                                       valid_calories)
            if isProductAdded:
                print(f"{OK}Product added successfully{Q}")
            else:
                print("{ER}Error adding product{Q}")
    helpers.enter_to_continue()


def update_product_name():
    """
    This function updates the name of a product from the google sheet
    """
    print(f"\n{OK}Update product name:{Q}\n")
    product_input = helpers.prepare_string(
        helpers.validate_length(input("Enter the product name: "),
                                "Enter the product name: ", 1, 20))
    products = productListGS.find_products_starting_with(product_input)
    prod = productListGS.find_product(product_input)
    if prod:
        conf_txt = f"Are you sure you want to update the name of {prod[0]}? "
        if not helpers.confirm(conf_txt + f"{OK}(y/n) or (yes/no){Q}: "):
            return
    elif len(products) == 0:
        print(f"{ER}Product not found{Q}")
        helpers.enter_to_continue()
        return
    elif len(products) > 1:
        print(f"{ER}Product not found{Q}")
        print("Did you mean one of these products?")
        for prod in products:
            print(prod[0] + ": " + prod[1])
        print("You must select one product")
        helpers.enter_to_continue()
        return
    elif len(products) == 1:
        conf_txt = f"Did you mean {products[0][0]}? "
        if helpers.confirm(conf_txt + f"{OK}(y/n) or (yes/no):{Q} "):
            prod = products[0]
        else:
            print(f"{OK}Product '{product_input}' not found{Q}")
            helpers.enter_to_continue()
            return

    new_product_name = helpers.prepare_string(helpers.validate_length(
        input("Enter the new product name: "),
        "Enter the product name to update: ", 1, 20))
    is_in_db = bool(productListGS.find_product(new_product_name))
    if is_in_db:
        print(f"{ER}Product {new_product_name} already exists{Q}")
        return
    productListGS.update_products(prod[0], new_product_name)
    print(f"{OK}Product {prod[0]} updated to {new_product_name}{Q}")
    helpers.enter_to_continue()


def update_product_calories():
    """
    This function updates the calories of a product from the google sheet
    """
    print(f"\n{OK}Update product calories:{Q}\n")
    product_input = helpers.prepare_string(helpers.validate_length(
        input("Enter the product name to update its calories: "),
        "Enter the product name to update its calories: ", 1, 20))
    products = productListGS.find_products_starting_with(product_input)
    prod = productListGS.find_product(product_input)
    if prod:
        conf_txt = f"Are you sure you want to update {prod[1]} "
        conf_txt += f" calories of {prod[0]}? "
        if not helpers.confirm(conf_txt + f"{OK}(y/n) or (yes/no):{Q} "):
            return
    elif len(products) == 0:
        print(f"{ER}Product not found{Q}")
        return
    elif len(products) > 1:
        print(f"{ER}Multiple products found{Q}")
        for prod in products:
            print(prod[0] + ": " + prod[1])
        print(f"{ER}You must select one product{Q}")
        return
    elif len(products) == 1:
        conf_txt = f"Did you mean {products[0][0]}? "
        if helpers.confirm(conf_txt + f"{OK}(y/n) or (yes/no):{Q} "):
            prod = products[0]
        else:
            print(f"{ER}Product '{product_input}' not found{Q}")
            helpers.enter_to_continue()
            return
    new_calories = helpers.is_number(input("Enter the new calories: "),
                                     "Enter the new calories: ")
    valid_calories = abs(int(new_calories))
    productListGS.update_products_calories(prod[0], valid_calories)
    txt = f"{OK}Calories of {prod[0]} updated to {valid_calories} calories{Q}"
    print(txt)
    helpers.enter_to_continue()


def update_product():
    """
    This function updates a product from the google sheet,
    it can update the name or the calories of the product
    """
    print(f"\n{OK}Update product, select:{Q}\n")
    helpers.log("1. Update a product name",
                "2. Update a product calories",
                "3. Go Back")
    option = helpers.select_option(update_product_name,
                                   update_product_calories)
    if option == 'exit':
        return 'exit'
    return option()


def delete_product():
    """
    This function deletes a product from the google sheet
    """
    print(f"\n{OK}Delete product:{Q}\n")
    product_input = helpers.prepare_string(
        input("Enter the product to delete: "))
    product = productListGS.find_product(product_input)
    if product:
        print(product[0] + ": " + product[1])
        conf_txt = f"Are you sure you want to delete {product[0]}? "
        if not helpers.confirm(conf_txt + f"{OK}(y/n) or (yes/no):{Q} "):
            return
        if productListGS.delete_product(product[0]):
            print(f"{OK}{product[0]} deleted{Q}")
    else:
        print(f"{ER}Product {product_input} not found{Q}")
    helpers.enter_to_continue()


# Manage personal data functions
def add_calculated_calories(calories, product, total_cal):
    print(f"\nCalories for {product} per 100 grams: " +
          calories + " calories\n")
    weight = abs(int(helpers.is_number(
        input("\nEnter the weight in grams: "),
        "\nEnter the weight in grams: ")))
    helpers.clear_terminal()
    calories = int(calories) * int(weight) / 100
    total_cal["calories"] += calories
    print(f"\nCalories for {product} per {weight} grams : "
          + str(round(calories)) + " calories")
    print(f"\nSum of calories for all products you have calculated: "
          + str(round(total_cal["calories"])) + " calories")
    cal_limit = googleSheetDB.get_calories_limit()
    cal_consumed = googleSheetDB.get_calories_consumed()
    cal_sum = int(cal_consumed) + int(total_cal["calories"])
    if bool(cal_limit) and cal_sum > int(cal_limit):
        over_limit_num = cal_sum - int(cal_limit)
        txt = f"\nIf you add these {round(total_cal['calories'])} cal, "
        txt += F"you will {ER}exceed your daily calories limit{Q} "
        print(txt + f"by {over_limit_num} cal\n")
    print("\n")
    conf_txt = f"Would you like to add {str(round(total_cal['calories']))} "
    conf_txt += "calories to your daily calories or"
    conf_txt += " would you like to continue?"
    conf_txt += "\nTo add and quit {OK}(y/yes){Q}, "
    conf_txt += f"to continue calculating {OK}(n/no){Q}: "
    if helpers.confirm(conf_txt):
        googleSheetDB.add_calories_consumed(round(total_cal['calories']))
        cal_consumed = googleSheetDB.get_calories_consumed()
        cal_limit = googleSheetDB.get_calories_limit()
        if bool(cal_limit) and int(cal_consumed) > int(cal_limit):
            over_limit_num = int(cal_consumed) - int(cal_limit)
            txt = f"\n{ER}You have exceeded your daily calories limit of "
            print(txt + f"{cal_limit} by {over_limit_num} calories{Q}\n")
        print(f"\nYou have consumed {cal_consumed} calories today")
        helpers.enter_to_continue()
        return True
    else:
        helpers.enter_to_continue()
        return False


def calculate_calories():
    """
    This function calculates the calories of the products entered by the user,
    if the product is not in the database,
    it will ask the user if he wants to add it
    """
    helpers.clear_terminal()
    total_calories = {"calories": 0}
    while True:
        txt = f"\n{OK}Calculate calories{Q}\n"
        txt += f"\nEnter {OK}product name{Q} or {OK}(q/quit){Q} to quit: "
        option = helpers.prepare_string(helpers.validate_length(
            input(txt), txt, 1, 20))
        helpers.clear_terminal()
        if option == "Q" or option == "Quit":
            return
        product = productListGS.find_product(option)
        products = productListGS.find_products_starting_with(option)
        if product:
            print(f"\n{OK}Product found{Q}")
            if add_calculated_calories(product[1], product[0], total_calories):
                return
            else:
                continue
        else:
            if len(products) == 1:
                txt = f" {OK}(y/n) or (yes/no){Q}: "
                if helpers.confirm(
                  f"\nDid you mean: {products[0][0]}?" + txt):
                    print("n")
                    if add_calculated_calories(products[0][1],
                                               products[0][0],
                                               total_calories):
                        return
                    else:
                        continue
                else:
                    print(f"\n{option} not found")
            if len(products) > 1:
                print(f"\n{ER}Product not found.{Q}\n")
                print("You probably meant something from this list:\n")
                for prod in products:
                    print(prod[0] + ": " + prod[1])
                helpers.enter_to_continue()
            else:
                print(f"{ER}\nProduct not found.{Q}\n")
                helpers.enter_to_continue()
            conf_txt = f"\nWould you like to add {option} to the database?"
            if helpers.confirm(f"{conf_txt} {OK}(y/n) or (yes/no):{Q} "):
                isProductAdded = productListGS.add_product(
                    option, abs(int(helpers.is_number(
                        input("\nEnter the calories: "),
                        "\nEnter the calories: "))))
                if isProductAdded:
                    print(f"\n{OK}{option} added successfully{Q}")
                    helpers.enter_to_continue()
                else:
                    print("Error adding product")
            else:
                print(f"\n{ER}{option} not added{Q}")
                helpers.enter_to_continue()


def set_calories_limit():
    """
    This function sets the calories limit of the user
    per day and writes it to the google sheet
    """
    print(f"\n{OK}Set calories limit:{Q}\n")
    calories_limit = helpers.is_number(
        input("Enter your calories limit per day: "),
        "Enter your calories limit per day: ")
    googleSheetDB.set_calories_limit(calories_limit)
    helpers.clear_terminal()
    print("Your new calories limit per day is " + calories_limit)
    helpers.enter_to_continue()


def add_consumed_calories():
    """
    This function adds the calories consumed by the user to the google sheet
    """
    print(f"\n{OK}Add consumed calories:{Q}\n")
    cal_consumed = googleSheetDB.get_calories_consumed()
    cal_limit = googleSheetDB.get_calories_limit()
    txt = "You have consumed " + cal_consumed + " calories today\n"
    txt += "How many more calories have you consumed today?:"
    txt += "\nEnter the calories: "
    cal_to_add = helpers.is_number(input(txt), txt)
    googleSheetDB.add_calories_consumed(abs(int(cal_to_add)))
    helpers.clear_terminal()
    print(f"\n{OK}Adding daily intake{Q}\n")
    cal_consumed = googleSheetDB.get_calories_consumed()
    print("You've consumed " + str(cal_consumed) + " calories so far")
    if bool(cal_limit) and int(cal_consumed) > int(cal_limit):
        over_limit_num = int(cal_consumed) - int(cal_limit)
        txt = F"You have {ER}exceeded your daily calories limit{Q} of "
        print(txt + f"{cal_limit} by {over_limit_num} calories")
    helpers.enter_to_continue()


def get_consumed_calories():
    """
    This function prints the calories consumed by the user
    """
    print(f"\n{OK}Get consumed calories:{Q}\n")
    cal_consumed = googleSheetDB.get_calories_consumed()
    cal_limit = googleSheetDB.get_calories_limit()
    if bool(cal_limit):
        over_limit_num = int(cal_consumed) - int(cal_limit)
        if int(cal_consumed) > int(cal_limit):
            txt = f"You have {ER}exceeded your daily calories limit{Q} of "
            print(txt + f"{cal_limit} by {over_limit_num} calories")
        elif int(cal_consumed) == int(cal_limit):
            txt = "You have reached your daily calories limit of "
            print(txt + f"{cal_limit} calories")
        else:
            cal_to_eat = int(cal_limit) - int(cal_consumed)
            txt = "To reach your daily calories limit you still have "
            print(txt + f"{OK}{str(cal_to_eat)} calories to consume today{Q}")
    print("You've consumed " + cal_consumed + " calories so far today")
    helpers.enter_to_continue()


def add_your_weight_in_kg():
    print(f"\n{OK}Add your weight in KG:{Q}\n")
    if googleSheetDB.add_weight(helpers.is_float(
        input("Enter your weight (kg): "),
            "Enter your weight (kg): "), "kg"):
        helpers.enter_to_continue()
    else:
        helpers.enter_to_continue()


def add_your_weight_in_lb():
    print(f"\n{OK}Add your weight in LB:{Q}\n")
    if googleSheetDB.add_weight(helpers.is_float(
        input("Enter your weight (lb): "),
            "Enter your weight (lb): "), "lb"):
        helpers.enter_to_continue()
    else:
        helpers.enter_to_continue()


def add_your_weight():
    """
    This function adds your weight to the google sheet
    """
    helpers.clear_terminal()
    while True:
        print(f"\n{OK}Add your weight, selcet:{Q}\n")
        helpers.log("1. Add your weight in kilograms (kg)",
                    "2. Add your weight in pounds (lb)",
                    "3. Go Back")
        option = helpers.select_option(add_your_weight_in_kg,
                                       add_your_weight_in_lb)
        if option == 'exit':
            helpers.clear_terminal()
            break
        option()


# Account management functions
def update_password():
    """
    This function updates the password of the user
    """
    print(f"\n{OK}Update your password{Q}\n")
    input_text = "Enter your new password: "
    new_password = helpers.validate_length(input(input_text),
                                           input_text, 6, 12, True)
    authGS.update_password(new_password)
    print(f"{OK}Your password has been updated{Q}")
    helpers.enter_to_continue()


def delete_account():
    """
    This function deletes the account of the user
    """
    print(f"\n{OK}Delete your account{Q}\n")
    txt = "Are you sure you want to delete your account? "
    if helpers.confirm(txt + f"{OK}(y/n) or (yes/no):{Q} "):
        username = authGS.username
        if authGS.delete_user():
            helpers.clear_terminal()
            print(f"\n{OK}Account deleted{Q}")
            print(f"\nGood bye {username}\n")
            exit()
        else:
            print("Error deleting account")
            helpers.enter_to_continue()
            return False
    else:
        print(f"{ER}Account not deleted{Q}")
        helpers.enter_to_continue()
        return False


def manage_account():
    """
    This function is the menu of the account management
    """
    helpers.clear_terminal()
    while True:
        print(f"\n{OK}Manage your account, select{Q}\n")
        helpers.log("1. Change password", "2. Delete account", "3. Go Back")
        option = helpers.select_option(update_password, delete_account)
        if option == 'exit':
            helpers.clear_terminal()
            break
        option()


def calculate_calories_limit():
    """
    This function calculates the calories limit of the user
    """
    print(f"\n{OK}Your calories limit{Q}\n")
    cal_limit = googleSheetDB.get_calories_limit()
    if not bool(cal_limit):
        print("You haven't set your calories limit yet")
        return
    consumed_cal = googleSheetDB.get_calories_consumed()
    cal_to_eat = int(cal_limit) - int(consumed_cal)
    txt = ""
    cal_limit_text = "Your calories limit a day is " + cal_limit + " calories"
    consumed_cal_text = "You've consumed " + consumed_cal + " calories today"
    if cal_to_eat < 0:
        abs_cal = abs(cal_to_eat)
        txt = f"{ER}You've consumed {abs_cal} cal more than your limit{Q}"
    elif cal_to_eat == 0:
        txt = f"You've consumed {consumed_cal}"
        txt += f" calories, {ER}you've reached your limit{Q}"
    else:
        txt = f"{OK}You can eat {cal_to_eat} calories more today{Q}"
    helpers.log(cal_limit_text, consumed_cal_text, txt)
    helpers.enter_to_continue()


# Progress functions

def calculate_progress(data):
    """
    Calculate progress from the Google Worksheet
    """
    try:
        print(f"\n{OK}Calculate your progress{Q}\n")
        first_weight = data[0][2]
        last_weight = data[-1][2]
        kg = float(first_weight) - float(last_weight)
        lb = round(kg * 2.20462, 1)
        first_date = data[0][0]
        last_date = data[-1][0]
        days = (last_date - first_date).days
        cal_list = [int(cal[1]) for cal in data]
        del cal_list[-1]
        avr_cal = round(sum(cal_list) / int(days))
        print("The result shows your progress from " +
              first_date.strftime("%d/%m/%Y") + " to "
              + last_date.strftime("%d/%m/%Y"))
        print("On average you ate " + str(avr_cal) + " calories a day")
        if kg > 0:
            print(f"You lost {kg} kg or {lb} lb in {days} days")
        elif kg < 0:
            print(f"You gained {kg} kg or {lb} lb in {days} days")
        else:
            print(f"You didn't gain or lose weight in {days} days")
        helpers.enter_to_continue()
    except IndexError as er:
        print(er)


def get_last_progress():
    """
    This function prints the last progress of the user
    """
    try:
        data = googleSheetDB.get_list_of_consecutive_days()
        if data:
            calculate_progress(data[-1])
        else:
            print(f"\n{OK}Calculate progress{Q}\n")
            print(f"\n{ER}Not enough data to calculate progress{Q}")
            print(f"{ER}Weight and calories intake data must be provided,{Q}"
                  f"{ER} at least 7 consecutive days{Q}\n")
            helpers.enter_to_continue()
    except IndexError:
        print(f"\n{OK}Calculate progress{Q}\n")
        print(f"\n{ER}Not enough data to calculate progress{Q}")
        print(f"{ER}Weight and calories intake data must be provided,{Q}"
              f" {ER}at least 7 consecutive days{Q}\n")
        helpers.enter_to_continue()


def view_progress_by_date():
    """
    This function prints the progress of the user by date
    """
    data = googleSheetDB.get_list_of_consecutive_days()
    helpers.clear_terminal()
    if data:
        list_of_functions = []
        log_text = []
        for index, row in enumerate(data):
            first_date = row[0][0].strftime('%d/%m/%Y')
            last_date = row[-1][0].strftime('%d/%m/%Y')
            log_text.append(f"{index + 1}. {first_date} - {last_date}")
            list_of_functions.append(
                helpers.wrapper_function(calculate_progress, row))
        log_text.append(f"{len(data) + 1}. Go Back")
        helpers.clear_terminal()
        while True:
            print(f"\n{OK}Calculate progress{Q}\n")
            helpers.log(*log_text)
            option = helpers.select_option(*list_of_functions)
            if option == 'exit':
                helpers.clear_terminal()
                break
            option()
    else:
        print(f"\n{OK}Calculate progress{Q}\n")
        print(f"\n{ER}Not enough data to calculate progress{Q}")
        print(f"{ER}Weight and calories intake data must be provided,{Q}"
              f"{ER} at least 7 consecutive days{Q}\n")
        helpers.enter_to_continue()


def see_progress():
    """
    This function is the menu that allows the user to see his progress
    """
    helpers.clear_terminal()
    while True:
        print(f"\n{OK}Calculate your progress{Q}\n")
        helpers.log("1. See your last progress",
                    "2. View your progress by date",
                    "3. Go Back")
        option = helpers.select_option(get_last_progress,
                                       view_progress_by_date)
        if option == 'exit':
            helpers.clear_terminal()
            break
        option()
