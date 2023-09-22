from python.googlesheet import googleSheetDB, authGS, productListGS
from python.helpers_func import clear_terminal, log, confirm, validate_length, is_number, prepare_string, select_option


def login():
    """
    This function logs in the user to the google sheet
    """
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
        print("Username already exists")
        return False


def add_new_product():
    """
    This function adds a new product to the google sheet, if the product already exists, it will not be added
    """
    if not confirm("Are you sure you want to add a new product? (y/n) or (yes/no): "):
        return
    validatedProduct = prepare_string(validate_length(input("Enter the product: "), "Enter the product: ", 1, 20))
    validatedCalories = is_number(input("Enter the calories: "), "Enter the calories: ")
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
    product = prepare_string(validate_length(input("Enter the product name to update: "), "Enter the product name to update: ", 1, 20))
    products = productListGS.find_products_starting_with(product)
    if len(products) == 0:
        print("Product not found")
        return
    elif len(products) > 1:
        print("Multiple products found, you must select one")
        for product in products:
            print(product[0] + ": " + product[1])
        return
    else:
        product = products[0][0]
        if not confirm(f"Are you sure you want to update a product name of {product}? (y/n) or (yes/no): "):
            return
    new_product = prepare_string(validate_length(input("Enter the new product name: "), "Enter the product name to update: ", 1, 20))
    is_in_db = bool(productListGS.find_product(new_product))
    if is_in_db:
        print(f"Product {new_product} already exists")
        return
    productListGS.update_products(product, new_product)
    print("Product " + product + " updated to " + new_product)


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
    new_calories = is_number(input("Enter the new calories: "), "Enter the new calories: ")
    productListGS.update_products_calories(product[0], new_calories)
    print("Calories of " + product[0] + " updated to " + new_calories + " calories")


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
    product = productListGS.find_product(prepare_string(input("Enter the product to delete: ")))
    if product:
        print(product[0] + ": " + product[1])
        if not confirm(f"Are you sure you want to delete {product[0]}? (y/n) or (yes/no): "):
            return
        if productListGS.delete_product(product[0]):
            print(f"{product[0]} deleted")


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
            break
        product = productListGS.find_product(option)
        products = productListGS.find_products_starting_with(option)
        if product:
            print(product[0] + ": " + product[1])
            weight = is_number(input("Enter the weight in grams : "), "Enter the weight in grams : ")
            calories = int(product[1]) * int(weight) / 100
            total_calories += calories
            print(f"Calories for {product[0]} per {weight} grams : " + str(round(calories)) + " calories")
            print(f"Sum of calories for products you have calculated: " + str(round(total_calories)) + " calories")
        else:
            print("Product not found")
            if len(products) > 0:
                print("Did you mean:")
                for prod in products:
                    print(prod[0] + ": " + prod[1])
            if confirm(f"Would you like to add {option} to our database? (y/n): "):
                clear_terminal()
                isProductAdded = productListGS.add_product(option, input("Enter the calories: "))
                if isProductAdded:
                    print(f"{option} added successfully")
                else:
                    print("Error adding product")
            else:
                clear_terminal()
                print(f"{option} not added")


def set_calories_limit():
    """
    This function sets the calories limit of the user per day and writes it to the google sheet
    """
    calories_limit = is_number(input("Enter your calories limit per day: "), "Enter your calories limit per day: ")
    googleSheetDB.set_calories_limit(calories_limit)
    clear_terminal()
    print("Your new calories limit per day is " + calories_limit )


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
        authGS.delete_user()
        print("Account deleted")
        return True
    else:
        print("Account not deleted")
        return False


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
