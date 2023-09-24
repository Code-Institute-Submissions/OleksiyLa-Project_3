import gspread
from google.oauth2.service_account import Credentials
import datetime
from python.helpers_func import confirm, enter_to_continue, clear_terminal

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]


class BasicGoogleSheetOperations:
    """
    Class that implements basic CRUD operations with Google Sheet
    """

    @staticmethod
    def connect(creds_file, scope, sheet_name):
        """
        Connect to Google Sheet
        """
        try:
            creds = Credentials.from_service_account_file(creds_file)
            scoped_creds = creds.with_scopes(scope)
            gspread_client = gspread.authorize(scoped_creds)
            sheet = gspread_client.open(sheet_name)
            BasicGoogleSheetOperations._sheet = sheet
            return True
        except Exception as error:
            print(f"Error connecting to Google Sheet: {str(error)}")


    def create_row(self, data, worksheet_name):
        """
        Create a new row in the Google Worksheet
        """
        try:
            BasicGoogleSheetOperations._sheet.worksheet(worksheet_name).append_row(data)
            return True
        except Exception as error:
            print(f"Error creating row: {str(error)}")
        return False


    def read_rows(self, worksheet_name):
        """
        Read all rows from the Google Worksheet
        """
        try:
            rows = BasicGoogleSheetOperations._sheet.worksheet(worksheet_name).get_all_values()
            return rows
        except Exception as error:
            print(f"Error reading rows: {str(error)}")
        return []


    def update_cell(self, to_update, updated, worksheet_name):
        """
        Update a row in the Google Worksheet
        """
        try:
            BasicGoogleSheetOperations._sheet.worksheet(worksheet_name).update_cell(to_update[0], to_update[1], updated)
            return True
        except Exception as error:
            print(f"Error updating row: {str(error)}")
        return False


    def delete_row(self, row_number, worksheet_name):
        """
        Delete a row from the Google Worksheet
        """
        try:
            BasicGoogleSheetOperations._sheet.worksheet(worksheet_name).delete_row(row_number)
            return True
        except Exception as error:
            print(f"Error deleting rows: {str(error)}")
        return False


    def add_worksheet(self, title, rows, cols):
        """
        Add a new worksheet to the Google Spreadsheet
        """
        try:
            BasicGoogleSheetOperations._sheet.add_worksheet(title=title, rows=rows, cols=cols)
            return True
        except Exception as error:
            print(f"Error adding worksheet: {str(error)}")


    def del_worksheet(self, username):
        """
        Delete a worksheet from the Google Spreadsheet
        """
        try:
            BasicGoogleSheetOperations._sheet.del_worksheet(BasicGoogleSheetOperations._sheet.worksheet(username))
            return True
        except Exception as error:
            print(f"Error deleting worksheet: {str(error)}")


class AuthGS(BasicGoogleSheetOperations):
    """
    Class that implements AUTH operations with Google Sheet
    """
    username = None


    def __init__(self):
        super().__init__()


    def login(self, username, password):
        """
        Login to the Google Worksheet
        """
        try:
            users = self.read_rows("users")
            for user in users:
                if user[0] == username and user[1] == password:
                    AuthGS.username = username
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
            data = [username, password]
            self.create_row(data, "users")
            self.add_worksheet(username, 500, 20)
            AuthGS.username = username
            return True
        except Exception as error:
            print(f"Error registering: {str(error)}")
        return False


    def update_password(self, password):
        """
        Update a user's password in the Google Worksheet
        """
        try:
            users = self.read_rows("users")
            for index, user in enumerate(users):
                if user[0] == AuthGS.username:
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
                if user[0] == AuthGS.username:
                    self.delete_row(index + 1, "users")
                    self.del_worksheet(AuthGS.username)
                    AuthGS.username = None
                    return True
        except Exception as error:
            print(f"Error deleting user: {str(error)}")
        return False


class ProductListGS(BasicGoogleSheetOperations):
    """
    Class that implements CRUD operations with Product List Google Sheet
    """
    def __init__(self):
        super().__init__()


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


class CaloriesTrackerGS(BasicGoogleSheetOperations):
    """
    Class that implements advanced operations with Google Sheet catered to the Calories Tracker App
    """
    def __init__(self):
        super().__init__()


    def set_calories_limit(self, calories_limit):
        """
        Set a user's calories limit in the Google Worksheet
        """
        try:
            users = self.read_rows("users")
            for index, user in enumerate(users):
                if user[0] == AuthGS.username:
                    self.update_cell([index + 1, 3], calories_limit, "users")
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
            user_worksheet = self.read_rows(AuthGS.username)
            for index, row in enumerate(user_worksheet):
                if row[0] == current_datetime:
                    calories = int(row[1]) + int(calories)
                    self.update_cell([index + 1, 2], calories, AuthGS.username)
                    return True
            data = [current_datetime, calories]
            self.create_row(data, AuthGS.username)
            return True
        except Exception as error:
            print(f"Error adding calories consumed: {str(error)}")
        return False


    def get_calories_consumed(self):
        """
        Get calories consumed per today from the Google Worksheet
        """
        for row in self.read_rows(AuthGS.username):
            try:
                if row[0] == datetime.datetime.now().strftime("%d/%m/%Y"):
                    return row[1]
            except:
                return "0"
        return "0"


    def get_calories_limit(self):
        """
        Get calories limit from the Google Worksheet
        """
        for row in self.read_rows("users"):
            if row[0] == AuthGS.username:
                try:
                    return row[2]
                except:
                    return None
        return None


    def add_weight(self, weight, unit):
        """
        Add weight to the Google Worksheet
        """
        if unit == "kg":
            weight_in_kilograms = round(float(weight), 1)
            prev_weight = 1
        if unit == "lb":
            weight_in_kilograms = round(float(weight) * 0.453592, 1)
            prev_weight = 2.20462
        try:
            current_datetime = datetime.datetime.now()
            current_datetime = current_datetime.strftime("%d/%m/%Y")
            user_worksheet = self.read_rows(AuthGS.username)
            for index, row in enumerate(user_worksheet):
                if row[0] == current_datetime:
                    if len(row) == 3:
                        prev_weight = round(prev_weight * float(row[2]), 1)
                        if round(float(row[2]), 1) == weight_in_kilograms:
                            print(f"You already added this weight of {weight} {unit} today")
                            return True
                        if confirm(f"You already added {prev_weight} {unit} today, do you want to update it to {weight} {unit}? ('y'/'yes') or ('n'/'no'): "):
                            if self.update_cell([index + 1, 3], weight_in_kilograms, AuthGS.username):
                                print(f"Weight updated to {weight} {unit} successfully")
                        else:
                            print(f"Weight of {prev_weight} {unit} not updated")
                    else:
                        if self.update_cell([index + 1, 3], weight_in_kilograms, AuthGS.username):
                            print("Weight added successfully")
                            print("You can check your weight history in the 'Get your weight' menu")
                    return True
            data = [current_datetime, 0, weight_in_kilograms]
            self.create_row(data, AuthGS.username)
            print("Weight added successfully")
            print("You can check your weight history in the 'Get your weight' menu")
            return True
        except Exception as error:
            print(f"Error adding weight: {str(error)}")
        return False
    
    def convert_row_into_date(self, row):
        """
        Convert row into date
        """
        date = row[0].split("/")
        return datetime.datetime(int(date[2]), int(date[1]), int(date[0]))


    def get_user_data_with_date(self):
        """
        Get user data with date from the Google Worksheet
        """
        try:
            user_data = self.read_rows(AuthGS.username)
            if len(user_data) > 0:
                filtered_user_data = []
                for row in user_data:
                    if len(row) == 3:
                        if row[1] != '' and row[2] != '':
                            filtered_user_data.append([self.convert_row_into_date(row), row[1], row[2]])
                return filtered_user_data
            else:
                return False
        except Exception as error:
            print(f"Error getting user data with date: {str(error)}")
        return False
    
    def get_list_of_consecutive_days(self):
        """
        Get the last consecutive days from the Google Worksheet
        """
        try:
            user_data = self.get_user_data_with_date()
            if not user_data:
                return []
            lists_of_consecutive_days = []
            consecutive_days = []
            for row in user_data:
                if not consecutive_days or row[0] - consecutive_days[-1][0] == datetime.timedelta(days=1):
                    consecutive_days.append(row)
                else:
                    if len(consecutive_days) >= 7:
                        lists_of_consecutive_days.append(consecutive_days[:])
                    consecutive_days = [row]

            if len(consecutive_days) >= 7:
                lists_of_consecutive_days.append(consecutive_days[:])

            return lists_of_consecutive_days
        except Exception as error:
            print(f"Error getting the last consecutive days: {str(error)}")
        return []


BasicGoogleSheetOperations.connect('creds.json', SCOPE, 'calories_tracker')
googleSheetDB = CaloriesTrackerGS()
authGS = AuthGS()
productListGS = ProductListGS()