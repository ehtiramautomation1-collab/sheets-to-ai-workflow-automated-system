from config.logging_configure import setup_loggging
from google.oauth2.service_account import Credentials
from datetime import datetime
import gspread
import uuid

logger = setup_loggging("gspreed_logger", "log/gspreed.log")

class Gspreed_Service:
    def __init__(self):
        logger.info("Google is initing service account auth for gspreadservice...")
        self.scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        self.token = Credentials.from_service_account_file(
            "credentials/google_credentials.json",
            scopes=self.scope
        )
        self.client = gspread.authorize(self.token)
        self.sheet = self.client.open("Shopinity_Sheet")
        self.working_sheet = self.sheet.get_worksheet(1)

    def get_sheet_Data(self):
        logger.info("Apps is now getting data from google spreadsheet...")
        records = self.working_sheet.get_all_records()
        logger.info("App has successfully got all data and returned to apps...")
        return records

    def create_requst(self, Product, Quatity, Price, email, adress):
        logger.info("Server is now creating spreadsheets request for customer data to store")
        request_ID = f"REQ-{uuid.uuid4().hex[:8].upper()}"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        row = [
            request_ID,
            timestamp,
            Product,
            Quatity,
            Price,
            email,
            adress,
            "Processing"
        ]
        logger.info("Created request successfully")
        self.working_sheet.append_row(row)
        return request_ID

    def update_request(self, req_id, status):
        logger.info("System is now updating the user request id in local db")
        records = self.working_sheet.get_all_records()
        for row_number, rec in enumerate(records, start=2):
            logger.info("System is now fetching data from existing records and finding match...")
            if rec["Request_ID"] == req_id:
                self.working_sheet.update_cell(row_number, 8, status)
                logger.info("Match found and data is updated")
                return True
        return False
