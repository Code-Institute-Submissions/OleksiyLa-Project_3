from googlesheet import googleSheetDB, authGS, productListGS

# helper functions
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

def confirm(yes, no):
    option = input(yes).lower()
    if option == "y" or option == "yes":
        return True
    elif option == "n" or option == "no":
        print(no)
        return False
    else:
        print("Wrong input, please type 'y' or 'n'")
        confirm()

def validate_length(data, input_message, min_length, max_length):
    if len(data.split(" ")) > 1:
        print("Input must not contain spaces")
        return validate_length(input(input_message), input_message, min_length, max_length)
    if len(data) < min_length:
        print(f"Input must be at least {min_length} characters long")
        return validate_length(input(input_message), input_message, min_length, max_length)
    elif len(data) > max_length:
        print(f"Input must be less than {max_length} characters long")
        return validate_length(input(input_message), input_message, min_length, max_length)
    else:
        return data
    

# main functions  
def auth():
    while True:
        log("Type '1' to login, '2' to register or '3' to exit", "Please select an option:", "1. Login", "2. Register", "3. Exit")
        option = input("Enter your option: ")
        if option == "1":
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            if authGS.login(username, password):
                print(f"Welcome {username}")
                return True
            else:
                print("Invalid username or password")
                return False
        elif option == "2":
            username = validate_length(input("Enter your username: "), "Enter your username: ", 2, 12)
            password = validate_length(input("Enter your password: "), "Enter your password: ", 6, 12)
            if authGS.register(username, password):
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
        log("Type '1' to create a new product", "Type '2' to read a product", "Type '3' to update a product", "Type '4' to delete a product", "Type '5' to go back to the main menu")
        log("1. Create a new product", "2. Read a product", "3. Update a product", "4. Delete a product", "5. Go Back")
        option = input("Enter your option: ")
        if option == "1":
            isProductAdded = productListGS.add_product(input("Enter the product: "), input("Enter the calories: "))
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
                product = input("Enter the product name to update: ")
                new_product = input("Enter the new product name: ")
                productListGS.update_products(product, new_product)
            elif option == "2":
                product = input("Enter the product to update: ")
                new_calories = input("Enter the new calories: ")
                productListGS.update_products_calories(product, new_calories)
            elif option == "3":
                break
        elif option == "4":
            product = productListGS.find_product(input("Enter the product to delete: "))
            if product:
                print(product[0] + ": " + product[1])
                option = input("Are you sure you want to delete this product? (y/n): ")
                if option == "y":
                    productListGS.delete_product(product[0])
                else:
                    print("Product not deleted")
        elif option == "5":
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
            crud()
        elif option == "2":
            calculate_calories()
        elif option == "3":
            manage_personal_info()
        elif option == "4":
            log_exit_message()
            break
        else:
            print("Invalid option, please type 1, 2 or 3")

def main():
    """
    Start the Calories Tracker App
    """
    print("Welcome to the Calories Tracker App")
    if auth():
        menu()

main()