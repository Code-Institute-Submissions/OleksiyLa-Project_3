from googlesheet import db

data = db.read_rows("list_of_products")
db.register("Oleksiy", "test")

def log_exit_message(username = ""):
    print("Thank you for using the Calories Tracker App")
    print(f"Goodbye {username}")
    
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
            if db.login(username, password):
                print(f"Welcome {username}")
                return username
            else:
                print("Invalid username or password")
        elif option == "2":
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            if db.register(username, password):
                print("Registration successful")
            else:
                print("Username already exists")
        elif option == "3":
            log_exit_message()
            break
        else:
            print("Invalid option, please type 1, 2 or 3")

def menu(username):
    while True:
        print("Type '1' for CRUD operations on list of products and calories table")
        print("Type '2' to calculate calories from typed food and its weight")
        print("Type '3' to access personal table")
        print("Type '4' to exit")
        option = input("Enter your option: ")
        if option == "1":
            print("Typed '1'")
        elif option == "2":
            print("Typed '2'")
        elif option == "3":
            print("Typed '3'")
        elif option == "4":
            log_exit_message(username)
            break
        else:
            print("Invalid option, please type 1, 2 or 3")

def main():
    """
    Start the Calories Tracker App
    """
    print("Welcome to the Calories Tracker App")
    username = auth()
    if username:
        menu(username)

main()