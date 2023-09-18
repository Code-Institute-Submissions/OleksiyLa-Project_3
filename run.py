from googlesheet import googleSheetDB

def log_exit_message():
    username = googleSheetDB.username
    print("Thank you for using the Calories Tracker App")
    if username is not None:
        print(f"Goodbye {username}")
    else:
        print("Goodbye")
    
def auth():
    while True:
        print("Type '1' to login, '2' to register or '3' to exit")
        print("Please select an option:")
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        option = input("Enter your option: ")
        if option == "1":
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            if googleSheetDB.login(username, password):
                print(f"Welcome {username}")
                return True
            else:
                print("Invalid username or password")
                return False
        elif option == "2":
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            if googleSheetDB.register(username, password):
                print("Registration successful")
            else:
                print("Username already exists")
        elif option == "3":
            log_exit_message()
            break
        else:
            print("Invalid option, please type 1, 2 or 3")

def crud():
    while True:
        print("Type '1' to create a new product")
        print("Type '2' to read a product")
        print("Type '3' to update a product")
        print("Type '4' to delete a product")
        print("Type '5' to go back to the main menu")
        print("1. Create a new product")
        print("2. Read a product")
        print("3. Update a product")
        print("4. Delete a product")
        print("5. Go Back")
        option = input("Enter your option: ")
        if option == "1":
            isProductAdded = googleSheetDB.add_product(input("Enter the product: "), input("Enter the calories: "))
            if isProductAdded:
                print("Product added successfully")
            else:
                print("Error adding product")
        elif option == "2":
            products = googleSheetDB.find_products_starting_with(input("Enter the product: "))
            for product in products:
                print(product[0] + ": " + product[1])
        elif option == "3":
            print("1. Update a product name")
            print("2. Update a product calories")
            print("3. Go Back")
            option = input("Enter your option: ")
            if option == "1":
                product = input("Enter the product name to update: ")
                new_product = input("Enter the new product name: ")
                googleSheetDB.update_products(product, new_product)
            elif option == "2":
                product = input("Enter the product to update: ")
                new_calories = input("Enter the new calories: ")
                googleSheetDB.update_products_calories(product, new_calories)
            elif option == "3":
                break
        elif option == "4":
            product = googleSheetDB.find_product(input("Enter the product to delete: "))
            if product:
                print(product[0] + ": " + product[1])
                option = input("Are you sure you want to delete this product? (y/n): ")
                if option == "y":
                    googleSheetDB.delete_product(product[0])
                else:
                    print("Product not deleted")
        elif option == "5":
            break
        else:
            print("Invalid option, please type 1, 2, 3, 4 or 5")

def calculate_calories():
    total_calories = 0
    while True:
        print("Type '1' to calculate calories from typed food and its weight")
        print("Type '2' to go back to the main menu")
        print("1. Calculate calories")
        print("2. Go Back")
        option = input("Enter your option: ")
        if option == "1":
            product = googleSheetDB.find_product(input("Enter the product: "))
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
                    isProductAdded = googleSheetDB.add_product(input("Enter the product: "), input("Enter the calories: "))
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
        print("Type '1' to set calories limit")
        print("Type '2' to go back to the main menu")
        print("1. Set calories limit")
        print("2. Go Back")
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
        print("Type '1' to change your password")
        print("Type '2' to delete your account")
        
        print("Type '3' to add calories consumed per today")
        print("Type '4' to set calories limit")
        print("Type '5' to see calories consumed per today")
        print("Type '6' to see calories limit")
        print("Type '7' to see your progress")
        print("Type '8' for our advice")

        print("Type '9' to go back to the main menu")
        
        print("1. Change password")
        print("2. Delete account")
        print("3. Add calories consumed per today")
        print("4. Set calories limit")
        print("5. See calories consumed per today")
        print("6. See calories limit")
        print("7. See your progress")
        print("8. Our advice")
        print("9. Go Back")
        option = input("Enter your option: ")
        if option == "1":
            password = input("Enter your new password: ")
            googleSheetDB.update_password(password)
        elif option == "2":
            option = input("Are you sure you want to delete your account? (y/n): ")
            if option == "y":
                googleSheetDB.delete_user()
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
            print("Are you sure you want to delete your account? (y/n): ")
        elif option == "8":
            print("Are you sure you want to delete your account? (y/n): ")
        elif option == "9":
            break
        else:
            print("Invalid option, please type 1,")

def menu():
    while True:
        if googleSheetDB.username is None:
            log_exit_message()
            return
        print("Type '1' for CRUD operations on list of products and their respective calories per 100g table")
        print("Type '2' to calculate calories from typed food and its weight")
        print("Type '3' to access personal info")
        print("Type '4' to exit")
        print("1. CRUD calories table")
        print("2. Calculate calories")
        print("3. Personal info")
        print("4. Exit")
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