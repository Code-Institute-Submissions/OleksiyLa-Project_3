from python.googlesheet import googleSheetDB, authGS, productListGS
from python.helpers_func import clear_terminal, log, confirm, validate_length, is_number, prepare_string, select_option, enter_to_continue


# Authentication functions
def login():
    """
    This function logs in the user to the google sheet
    """
    print("Login:")
    username = validate_length(input("Enter your username: "), "Enter your username: ", 2, 12, True)
    password = validate_length(input("Enter your password: "), "Enter your password: ", 6, 12, True)
    if authGS.login(username, password):
        clear_terminal()
        print(f"Welcome {username}")
        return True
    else:
        clear_terminal()
        print("Invalid username or password")
        return False


def register():
    """
    This function registers a new user to the google sheet, if the username already exists, it will not be added
    """
    print("Register:")
    username = validate_length(input("Enter your username: "), "Enter your username: ", 2, 12, True)
    password = validate_length(input("Enter your password: "), "Enter your password: ", 6, 12, True)
    if authGS.register(username, password):
        clear_terminal()
        log("Registration successful", f"Welcome {username}")
        return True
    else:
        clear_terminal()
        print(f"Username '{username}' already exists, try again")
        return register()


# Product table functions (CRUD)
def add_new_product():
    """
    This function adds a new product to the google sheet, if the product already exists, it will not be added
    """
    validatedProduct = prepare_string(validate_length(input("Enter the product: "), "Enter the product: ", 1, 20))
    if not confirm(f"Are you sure you want to add a new product '{validatedProduct}'? (y/n) or (yes/no): "):
        return
    validatedCalories = is_number(input("Enter the calories: "), "Enter the calories: ")
    validatedCalories = abs(int(validatedCalories))
    if productListGS.find_product(validatedProduct):
        print(f"Product {validatedProduct} already exists")
        return
    isProductAdded = productListGS.add_product(validatedProduct, validatedCalories)
    if isProductAdded:
        print("Product added successfully")
    else:
        print("Error adding product")


def read_product():
    validatedProducts = prepare_string(validate_length(input("Enter the product: "), "Enter the product: ", 1, 20))
    products = productListGS.find_products_starting_with(validatedProducts)
    for product in products:
        print(product[0] + ": " + product[1])


def update_product_name():
    """
    This function updates the name of a product from the google sheet
    """
    product_input = prepare_string(validate_length(input("Enter the product name to update: "), "Enter the product name to update: ", 1, 20))
    products = productListGS.find_products_starting_with(product_input)
    product = productListGS.find_product(product_input)
    if product:
        if not confirm(f"Are you sure you want to update the name of {product[0]}? (y/n) or (yes/no): "):
            return
    elif len(products) == 0:
        print("Product not found")
        return
    elif len(products) > 1:
        print("Multiple products found")
        for product in products:
            print(product[0] + ": " + product[1])
        print("You must select one product")
        return
    elif len(products) == 1:
        if confirm(f"Did you mean {products[0][0]}? (y/n) or (yes/no): "):
            product = products[0]
        else:
            print(f"Product '{product_input}' not found")
            return

    new_product_name = prepare_string(validate_length(input("Enter the new product name: "), "Enter the product name to update: ", 1, 20))
    is_in_db = bool(productListGS.find_product(new_product_name))
    if is_in_db:
        print(f"Product {new_product_name} already exists")
        return
    productListGS.update_products(product[0], new_product_name)
    print("Product " + product[0] + " updated to " + new_product_name)


def update_product_calories():
    """
    This function updates the calories of a product from the google sheet
    """
    product_input = prepare_string(validate_length(input("Enter the product name to update its calories: "), "Enter the product name to update its calories: ", 1, 20))
    products = productListGS.find_products_starting_with(product_input)
    product = productListGS.find_product(product_input)
    if product:
        if not confirm(f"Are you sure you want to update the {product[1]} calories of {product[0]}? (y/n) or (yes/no): "):
            return
    elif len(products) == 0:
        print("Product not found")
        return
    elif len(products) > 1:
        print("Multiple products found")
        for product in products:
            print(product[0] + ": " + product[1])
        print("You must select one product")
        return
    elif len(products) == 1:
        if confirm(f"Did you mean {products[0][0]}? (y/n) or (yes/no): "):
            product = products[0]
        else:
            print(f"Product '{product_input}' not found")
            return
    new_calories = is_number(input("Enter the new calories: "), "Enter the new calories: ")
    validatedCalories = abs(int(new_calories))
    productListGS.update_products_calories(product[0], validatedCalories)
    print("Calories of " + product[0] + " updated to " + str(validatedCalories) + " calories")


def update_product():
    """
    This function updates a product from the google sheet, it can update the name or the calories of the product
    """
    log("1. Update a product name", "2. Update a product calories", "3. Go Back")
    option = select_option(update_product_name, update_product_calories)
    if option == 'exit':
        return 'exit'
    return option()


def delete_product():
    """
    This function deletes a product from the google sheet
    """
    product_input = prepare_string(input("Enter the product to delete: "))
    product = productListGS.find_product(product_input)
    if product:
        print(product[0] + ": " + product[1])
        if not confirm(f"Are you sure you want to delete {product[0]}? (y/n) or (yes/no): "):
            return
        if productListGS.delete_product(product[0]):
            print(f"{product[0]} deleted")
    else:
        print(f"Product {product_input} not found")


# Personal info functions
def calculate_calories():
    """
    This function calculates the calories of the products entered by the user, 
    if the product is not in the database, it will ask the user if he wants to add it
    """
    clear_terminal()
    total_calories = 0
    while True:
        option = prepare_string(validate_length(input("Enter product name or (q/quit) to quit: "), "Enter product name or (q/quit) to quit: ", 1, 20))
        clear_terminal()
        if option == "Q" or option == "Quit":
            return
        product = productListGS.find_product(option)
        products = productListGS.find_products_starting_with(option)
        if product:
            weight = abs(int(is_number(input("Enter the weight in grams : "), "Enter the weight in grams : ")))
            calories = int(product[1]) * int(weight) / 100
            total_calories += calories
            print(f"Calories for {product[0]} per {weight} grams : " + str(round(calories)) + " calories")
            print(f"Sum of calories for all products you have calculated: " + str(round(total_calories)) + " calories")
            calories_limit = googleSheetDB.get_calories_limit()
            calories_consumed = googleSheetDB.get_calories_consumed()
            if bool(calories_limit) and int(calories_consumed) + int(total_calories) > int(calories_limit):
                over_limit_num = int(calories_consumed) + int(total_calories) - int(calories_limit)
                print(f"If you add these {round(total_calories)} calories, you will exceed your daily calories limit by {over_limit_num} calories")
            if confirm(f"Would you like to add {str(round(total_calories))} calories to your daily calories? (y/n): "):
                googleSheetDB.add_calories_consumed(round(total_calories))
                calories_consumed = googleSheetDB.get_calories_consumed()
                print(f"You have consumed {calories_consumed} calories today")
                enter_to_continue()
                return
            else:
                print(f"{str(round(total_calories))} calories not added")
                enter_to_continue()
                continue
        else:
            if len(products) == 1:
                if confirm(f"Did you mean: {products[0][0]}? (y/n) or (yes/no): "):
                    weight = abs(int(is_number(input("Enter the weight in grams : "), "Enter the weight in grams : ")))
                    calories = int(products[0][1]) * int(weight) / 100
                    total_calories += calories
                    print(f"Calories for {products[0][0]} per {weight} grams : " + str(round(calories)) + " calories")
                    print(f"Sum of calories for all products you have calculated: " + str(round(total_calories)) + " calories")
                    calories_limit = googleSheetDB.get_calories_limit()
                    calories_consumed = googleSheetDB.get_calories_consumed()
                    if bool(calories_limit) and int(calories_consumed) + int(total_calories) > int(calories_limit):
                        over_limit_num = int(calories_consumed) + int(total_calories) - int(calories_limit)
                        print(f"If you add these {round(total_calories)} calories, you will exceed your daily calories limit by {over_limit_num} calories")
                    if confirm(f"Would you like to add {str(round(total_calories))} calories to your daily calories? (y/n): "):
                        googleSheetDB.add_calories_consumed(round(total_calories))
                        calories_consumed = googleSheetDB.get_calories_consumed()
                        print(f"You have consumed {calories_consumed} calories today")
                        enter_to_continue()
                        return
                    else:
                        print(f"{str(round(total_calories))} calories not added")
                        enter_to_continue()
                        continue
                else:
                    print(f"{option} not found")
            if len(products) > 1:
                print("Product not found. You probably meant something from this list:")
                for prod in products:
                    print(prod[0] + ": " + prod[1])
                enter_to_continue()
            if confirm(f"Would you like to add {option} to the database? (y/n): "):
                isProductAdded = productListGS.add_product(option, abs(int(is_number(input("Enter the calories: "), "Enter the calories: "))))
                if isProductAdded:
                    print(f"{option} added successfully")
                    enter_to_continue()
                else:
                    print("Error adding product")
            else:
                print(f"{option} not added")
                enter_to_continue()


def set_calories_limit():
    """
    This function sets the calories limit of the user per day and writes it to the google sheet
    """
    calories_limit = is_number(input("Enter your calories limit per day: "), "Enter your calories limit per day: ")
    googleSheetDB.set_calories_limit(calories_limit)
    clear_terminal()
    print("Your new calories limit per day is " + calories_limit )


def add_consumed_calories():
    """
    This function adds the calories consumed by the user to the google sheet
    """
    calories_consumed = googleSheetDB.get_calories_consumed()
    input_text = f"You have consumed " + calories_consumed + " calories today, would you like to add more calories?:"
    calories_to_add = is_number(input(input_text), input_text)
    googleSheetDB.add_calories_consumed(calories_to_add)
    clear_terminal()
    calories_consumed = googleSheetDB.get_calories_consumed()
    print("You've consumed " + str(calories_consumed) + " calories so far")


def get_consumed_calories():
    """
    This function prints the calories consumed by the user
    """
    calories_consumed = googleSheetDB.get_calories_consumed()
    clear_terminal()
    print("You've consumed " + calories_consumed + " calories today")


def calculate_calories_limit():
    """
    This function calculates the calories limit of the user
    """
    calories_limit = googleSheetDB.get_calories_limit()
    if not bool(calories_limit):
        clear_terminal()
        print("You haven't set your calories limit yet")
        return
    consumed_calories = googleSheetDB.get_calories_consumed()
    calories_to_eat = int(calories_limit) - int(consumed_calories)
    calories_to_eat_text = ""
    calories_limit_text = "Your calories limit a day is " + calories_limit + " calories"
    consumed_calories_text = "You've consumed " + consumed_calories + " calories today"
    if calories_to_eat < 0:
        calories_to_eat_text = f"You've consumed {abs(calories_to_eat)} calories more than your limit"
    elif calories_to_eat == 0:
        calories_to_eat_text = f"You've consumed {consumed_calories} calories, you've reached your limit"
    else:
        calories_to_eat_text = f"You can eat {calories_to_eat} calories more today"
    clear_terminal()
    log(calories_limit_text, consumed_calories_text, calories_to_eat_text)


def calculate_overall_progress():
    """
    This function calculates the overall progress of the user
    """
    clear_terminal()
    print(googleSheetDB.calculate_overall_progress())


def add_your_weight():
    """
    This function adds your weight to the google sheet
    """
    clear_terminal()
    googleSheetDB.add_weight(is_number(input("Enter your weight: "), "Enter your weight: "))


# Account management functions
def update_password():
    """
    This function updates the password of the user
    """
    input_text = "Enter your new password: "
    new_password = validate_length(input(input_text), input_text, 6, 12, True)
    authGS.update_password(new_password)
    clear_terminal()
    print("Your password has been updated")


def delete_account():
    """
    This function deletes the account of the user
    """
    option = "Are you sure you want to delete your account? (y/n) or (yes/no): "
    clear_terminal()
    if confirm(option):
        username = authGS.username
        if authGS.delete_user():
            print("Account deleted")
            print(f"Good bye {username}")
            exit()
        else:
            print("Error deleting account")
            return False
    else:
        print("Account not deleted")
        return False
def manage_account():
    """
    This function is the menu of the account management
    """
    clear_terminal()
    while True:
        log("1. Change password", "2. Delete account", "3. Go Back")
        option = select_option(update_password, delete_account)
        if option == 'exit':
            clear_terminal()
            break
        option()