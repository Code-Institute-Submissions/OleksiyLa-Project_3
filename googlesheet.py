import gspread
from google.oauth2.service_account import Credentials
import datetime

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

class BasicGoogleSheetOperations:
    """
    Class that implements basic CRUD operations with Google Sheet
    """
    def __init__(self):
        self.sheet = None

    def connect(self, creds_file, scope, sheet_name):
        """
        Connect to Google Sheet
        """
        try:
            creds = Credentials.from_service_account_file(creds_file)
            scoped_creds = creds.with_scopes(scope)
            gspread_client = gspread.authorize(scoped_creds)
            sheet = gspread_client.open(sheet_name)
            self.sheet = sheet
            return True
        except Exception as error:
            print(f"Error connecting to Google Sheet: {str(error)}")

    def create_row(self, data, worksheet_name):
        """
        Create a new row in the Google Worksheet
        """
        try:
            self.sheet.worksheet(worksheet_name).append_row(data)
            return True
        except Exception as error:
            print(f"Error creating row: {str(error)}")
        return False

    def read_rows(self, worksheet_name):
        """
        Read all rows from the Google Worksheet
        """
        try:
            rows = self.sheet.worksheet(worksheet_name).get_all_values()
            return rows
        except Exception as error:
            print(f"Error reading rows: {str(error)}")
        return []

    def update_cell(self, to_update, updated, worksheet_name):
        """
        Update a row in the Google Worksheet
        """
        try:
            self.sheet.worksheet(worksheet_name).update_cell(to_update[0], to_update[1], updated)
            return True
        except Exception as error:
            print(f"Error updating row: {str(error)}")
        return False

    def delete_row(self, row_number, worksheet_name):
        """
        Delete a row from the Google Worksheet
        """
        try:
            self.sheet.worksheet(worksheet_name).delete_row(row_number)
            return True
        except Exception as error:
            print(f"Error deleting rows: {str(error)}")
        return False
    
    def add_worksheet(self, title, rows, cols):
        """
        Add a new worksheet to the Google Spreadsheet
        """
        try:
            self.sheet.add_worksheet(title=title, rows=rows, cols=cols)
            return True
        except Exception as error:
            print(f"Error adding worksheet: {str(error)}")

    def del_worksheet(self, username):
        """
        Delete a worksheet from the Google Spreadsheet
        """
        try:
            self.sheet.del_worksheet(self.sheet.worksheet(username))
            return True
        except Exception as error:
            print(f"Error deleting worksheet: {str(error)}")


class CaloriesTrackerGS(BasicGoogleSheetOperations):
    """
    Class that implements advanced operations with Google Sheet catered to the Calories Tracker App
    """
    def __init__(self):
        super().__init__()
        self.username = None

    def login(self, username, password):
        """
        Login to the Google Worksheet
        """
        try:
            users = self.read_rows("users")
            for user in users:
                if user[0] == username and user[1] == password:
                    self.username = username
                    return username
        except Exception as error:
            print(f"Error logging in: {str(error)}")
        return False
    
    def register(self, username, password):
        """
        Register a new user in the Google Worksheet
        """
        try:
            users = self.read_rows("users")
            for user in users:
                if user[0] == username:
                    return False
            current_datetime = datetime.datetime.now()
            current_datetime = current_datetime.strftime("%d/%m/%Y")
            data = [username, password, current_datetime]
            self.create_row(data, "users")
            self.add_worksheet(username, 500, 20)
            return True
        except Exception as error:
            print(f"Error registering: {str(error)}")
        return False
    
    def add_product(self, product, calories):
        """
        Add a new product to the Google Worksheet
        """
        try:
            data = [product, calories]
            self.create_row(data, "list_of_products")
            return True
        except Exception as error:
            print(f"Error adding product: {str(error)}")
        return False
    
    def delete_product(self, product):
        """
        Delete a product from the Google Worksheet
        """
        try:
            products = self.read_rows("list_of_products")
            for index, prod in enumerate(products):
                print(index)
                print(prod)
                if prod[0] == product:
                    self.delete_row(index + 1, "list_of_products")
                    return True
        except Exception as error:
            print(f"Error deleting product: {str(error)}")
        return False
    
    def update_products_calories(self, product, calories):
        """
        Update a product's calories in the Google Worksheet
        """
        try:
            products = self.read_rows("list_of_products")
            for index, prod in enumerate(products):
                if prod[0] == product:
                    self.update_cell([index + 1, 2], calories, "list_of_products")
                    return True
        except Exception as error:
            print(f"Error updating product: {str(error)}")
        return False
    
    def update_products(self, product, new_product):
        """
        Update a product in the Google Worksheet
        """
        try:
            products = self.read_rows("list_of_products")
            for index, prod in enumerate(products):
                if prod[0] == product:
                    self.update_cell([index + 1, 1], new_product, "list_of_products")
                    return True
        except Exception as error:
            print(f"Error updating product: {str(error)}")
        return False
    
    def update_password(self, password):
        """
        Update a user's password in the Google Worksheet
        """
        try:
            users = self.read_rows("users")
            for index, user in enumerate(users):
                if user[0] == self.username:
                    self.update_cell([index + 1, 2], password, "users")
                    return True
        except Exception as error:
            print(f"Error updating password: {str(error)}")
        return False
        
    def delete_user(self):
        """
        Delete a user from the Google Worksheet
        """
        try:
            users = self.read_rows("users")
            for index, user in enumerate(users):
                if user[0] == self.username:
                    self.delete_row(index + 1, "users")
                    self.del_worksheet(self.username)
                    self.username = None
                    return True
        except Exception as error:
            print(f"Error deleting user: {str(error)}")
        return False
    
    def find_product(self, product):
        """
        Find a product in the Google Worksheet
        """
        try:
            products = self.read_rows("list_of_products")
            for prod in products:
                if prod[0] == product:
                    return prod
        except Exception as error:
            print(f"Error finding product: {str(error)}")
        return False
    
    def find_products_starting_with(self, string):
        """
        Find a product in the Google Worksheet
        """
        try:
            products = self.read_rows("list_of_products")
            found_products = []
            for prod in products:
                if string in prod[0]:
                    found_products.append(prod)
            return found_products
        except Exception as error:
            print(f"Error finding product: {str(error)}")
        return False

    def set_calories_limit(self, calories_limit):
        """
        Set a user's calories limit in the Google Worksheet
        """
        try:
            users = self.read_rows("users")
            for index, user in enumerate(users):
                if user[0] == self.username:
                    self.update_cell([index + 1, 4], calories_limit, "users")
                    return True
        except Exception as error:
            print(f"Error setting calories limit: {str(error)}")
        return False
    
    def add_calories_consumed(self, calories):
        """
        Add calories consumed per day to the Google Worksheet
        """
        try:
            current_datetime = datetime.datetime.now()
            current_datetime = current_datetime.strftime("%d/%m/%Y")
            user_worksheet = self.read_rows(self.username)
            for index, row in enumerate(user_worksheet):
                if row[0] == current_datetime:
                    calories = int(row[1]) + int(calories)
                    self.update_cell([index + 1, 2], calories, self.username)
                    return True
            data = [current_datetime, calories]
            self.create_row(data, self.username)
            return True
        except Exception as error:
            print(f"Error adding calories consumed: {str(error)}")
        return False
    
    def get_calories_consumed(self):
        """
        Get calories consumed per today from the Google Worksheet
        """
        for row in self.read_rows(self.username):
            if row[0] == datetime.datetime.now().strftime("%d/%m/%Y"):
                return row[1]

    def get_calories_limit(self):
        """
        Get calories limit from the Google Worksheet
        """
        for row in self.read_rows("users"):
            if row[0] == self.username:
                try:
                    return f"{row[3]} calories"
                except:
                    return "not set"
          
    def add_weight(self, weight):
        """
        Add weight to the Google Worksheet
        """
        try:
            current_datetime = datetime.datetime.now()
            current_datetime = current_datetime.strftime("%d/%m/%Y")
            user_worksheet = self.read_rows(self.username)
            for index, row in enumerate(user_worksheet):
                if row[0] == current_datetime:
                    self.update_cell([index + 1, 3], weight, self.username)
                    return True
            data = [current_datetime, 0, weight]
            self.create_row(data, self.username)
            return True
        except Exception as error:
            print(f"Error adding weight: {str(error)}")
        return False


googleSheetDB = CaloriesTrackerGS()
googleSheetDB.connect('creds.json', SCOPE, 'calories_tracker')