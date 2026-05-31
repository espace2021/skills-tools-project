import gspread
from google.oauth2.service_account import Credentials

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file(
    "data/credentials.json",
    scopes=scope
)

client = gspread.authorize(creds)

SPREADSHEET_IDS = {
    "voitures":   "1HyPcG2WJxEXbcE6eU7QMqUHw0t-oe_AmBO_VmwBzXGs",
    "clients":    "1L8AxrpOambXjabiPCW_Ht-TRtEzmERCg7EUnJzPVZMs",
    "promotions": "1zuFcYOmXM9J5qEx8GKEcVTMT_Jhl77rsjznvpRJC4aw",
}


def get_sheet_records(sheet_name):
    sheet = client.open_by_key(
        SPREADSHEET_IDS[sheet_name]
    ).sheet1

    return sheet.get_all_records()


