import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

class GoogleSheet:
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
            print(f"Error updating row")
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


db = GoogleSheet()
db.connect('creds.json', SCOPE, 'calories_tracker')