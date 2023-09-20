from googlesheet import googleSheetDB, authGS, productListGS
import os

# helper functions
def clear_terminal():
    """
      Check the operating system and use the appropriate clear command
    """
    if os.name == 'posix':
        os.system('clear')
    elif os.name == 'nt':
        os.system('cls')

def log_exit_message():
    username = authGS.username
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


# main functions  
def auth():
    while True:
        log("Type '1' to login, '2' to register or '3' to exit", "Please select an option:", "1. Login", "2. Register", "3. Exit")
        option = input("Enter your option: ")
        if option == "1":
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            if authGS.login(username, password):
                clear_terminal()
                print(f"Welcome {username}")
                return True
            else:
                print("Invalid username or password")
                return False
        elif option == "2":
            username = validate_length(input("Enter your username: "), "Enter your username: ", 2, 12, True)
            password = validate_length(input("Enter your password: "), "Enter your password: ", 6, 12, True)
            if authGS.register(username, password):
                clear_terminal()
                log("Registration successful", f"Welcome {username}")
                return True
            else:
                print("Username already exists")
        elif option == "3":
            log_exit_message()
            break
        else:
            print("Invalid option, please type 1, 2 or 3")

def crud():
    while True:
        log("1. Create a new product", "2. Read a product", "3. Update a product", "4. Delete a product", "5. Go Back")
        option = input("Enter your option: ")
        if option == "1":
            if not confirm("Are you sure you want to add a new product? (y/n) or (yes/no): "):
                continue
            validatedProduct = validate_length(input("Enter the product: "), "Enter the product: ", 2, 20)
            validatedCalories = is_number(input("Enter the calories: "), "Enter the calories: ")
            isProductAdded = productListGS.add_product(validatedProduct, validatedCalories)
            if isProductAdded:
                print("Product added successfully")
            else:
                print("Error adding product")
        elif option == "2":
            products = productListGS.find_products_starting_with(input("Enter the product: "))
            for product in products:
                print(product[0] + ": " + product[1])
        elif option == "3":
            log("1. Update a product name", "2. Update a product calories", "3. Go Back")
            option = input("Enter your option: ")
            if option == "1":
                product = validate_length(input("Enter the product name to update: "), "Enter the product name to update: ", 2, 20)
                products = productListGS.find_products_starting_with(product)
                if len(products) == 0:
                    print("Product not found")
                    continue
                elif len(products) > 1:
                    print("Multiple products found, you must select one")
                    for product in products:
                        print(product[0] + ": " + product[1])
                    continue
                else:
                    product = products[0][0]
                    if not confirm(f"Are you sure you want to update a product name of {product}? (y/n) or (yes/no): "):
                        continue
                new_product = validate_length(input("Enter the new product name: "), "Enter the product name to update: ", 2, 20)
                is_in_db = bool(productListGS.find_product(new_product))
                if is_in_db:
                    print(f"Product {new_product} already exists")
                    continue
                productListGS.update_products(product, new_product)
                print("Product " + product + " updated to " + new_product)
            elif option == "2":
                product_input = validate_length(input("Enter the product name to update its calories: "), "Enter the product name to update its calories: ", 2, 20)
                products = productListGS.find_products_starting_with(product_input)
                product = productListGS.find_product(product_input)
                if product:
                    if not confirm(f"Are you sure you want to update the {product[1]} calories of {product[0]}? (y/n) or (yes/no): "):
                        continue
                elif len(products) == 0:
                    print("Product not found")
                    continue
                elif len(products) > 1:
                    print("Multiple products found")
                    for product in products:
                        print(product[0] + ": " + product[1])
                    print("You must select one product")
                    continue

                new_calories = is_number(input("Enter the new calories: "), "Enter the new calories: ")
                productListGS.update_products_calories(product[0], new_calories)
                print("Calories of " + product[0] + " updated to " + new_calories + " calories")
            elif option == "3":
                clear_terminal()
                break
        elif option == "4":
            product = productListGS.find_product(input("Enter the product to delete: "))
            if product:
                print(product[0] + ": " + product[1])
                if not confirm(f"Are you sure you want to delete {product[0]}? (y/n) or (yes/no): "):
                    continue
                if productListGS.delete_product(product[0]):
                    print(f"{product[0]} deleted")
        elif option == "5":
            clear_terminal()
            break
        else:
            print("Invalid option, please type 1, 2, 3, 4 or 5")

def calculate_calories():
    total_calories = 0
    while True:
        log("1. Calculate calories", "2. Go Back")
        option = input("Enter your option: ")
        if option == "1":
            product = productListGS.find_product(input("Enter the product: "))
            if product:
                print(product[0] + ": " + product[1])
                weight = input("Enter the weight: ")
                calories = int(product[1]) * int(weight) / 100
                total_calories += calories
                print(f"Calories for {product[0]} per {weight}gramm : " + str(calories))
                print(f"Sum of calories for products you have calculated: " + str(total_calories))
            else:
                print("Product not found")
                option = input("Would you like to add this product to our database? (y/n): ")
                if option == "y":
                    isProductAdded = productListGS.add_product(input("Enter the product: "), input("Enter the calories: "))
                    if isProductAdded:
                        print("Product added successfully")
                    else:
                        print("Error adding product")              
        elif option == "2":
            clear_terminal()
            break
        else:
            print("Invalid option, please type 1 or 2")

def set_calories_limit():
    while True:
        log("1. Set calories limit", "2. Go Back")
        option = input("Enter your option: ")
        if option == "1":
            calories_limit = input("Enter your calories limit: ")
            googleSheetDB.set_calories_limit(calories_limit)
        elif option == "2":
            clear_terminal()
            break
        else:
            print("Invalid option, please type 1 or 2")

def manage_personal_info():
    while True:
        log("1. Change password", "2. Delete account", "3. Add calories consumed per today", "4. Set calories limit", "5. See calories consumed per today", "6. See calories limit", "7. See your progress", "8. Add your weight", "9. Go Back")
        option = input("Enter your option: ")
        if option == "1":
            password = input("Enter your new password: ")
            authGS.update_password(password)
        elif option == "2":
            option = input("Are you sure you want to delete your account? (y/n): ")
            if option == "y":
                authGS.delete_user()
                break
            else:
                print("Account not deleted")
        elif option == "3":
            calories_consumed = input("Enter how many calories you have consumed this day: ")
            googleSheetDB.add_calories_consumed(calories_consumed)
        elif option == "4":
            googleSheetDB.set_calories_limit(input("Enter your calories limit per day: "))
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
            log_exit_message()
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
            log_exit_message()
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