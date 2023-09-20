from googlesheet import googleSheetDB, authGS, productListGS
from helpers_func import clear_terminal, log_exit_message, log, confirm, validate_length, is_number, prepare_string, select_option

def login():
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
    if not confirm("Are you sure you want to add a new product? (y/n) or (yes/no): "):
        return
    validatedProduct = prepare_string(validate_length(input("Enter the product: "), "Enter the product: ", 2, 20))
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
    validatedProducts = prepare_string(validate_length(input("Enter the product: "), "Enter the product: ", 2, 20))
    products = productListGS.find_products_starting_with(validatedProducts)
    for product in products:
        print(product[0] + ": " + product[1])

def update_product_name():
    product = prepare_string(validate_length(input("Enter the product name to update: "), "Enter the product name to update: ", 2, 20))
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
    new_product = prepare_string(validate_length(input("Enter the new product name: "), "Enter the product name to update: ", 2, 20))
    is_in_db = bool(productListGS.find_product(new_product))
    if is_in_db:
        print(f"Product {new_product} already exists")
        return
    productListGS.update_products(product, new_product)
    print("Product " + product + " updated to " + new_product)

def update_product_calories():
    product_input = prepare_string(validate_length(input("Enter the product name to update its calories: "), "Enter the product name to update its calories: ", 2, 20))
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
    log("1. Update a product name", "2. Update a product calories", "3. Go Back")
    option = select_option(update_product_name, update_product_calories)
    if option == 'exit':
        return 'exit'
    return option()

def delete_product():
    product = productListGS.find_product(prepare_string(input("Enter the product to delete: ")))
    if product:
        print(product[0] + ": " + product[1])
        if not confirm(f"Are you sure you want to delete {product[0]}? (y/n) or (yes/no): "):
            return
        if productListGS.delete_product(product[0]):
            print(f"{product[0]} deleted")