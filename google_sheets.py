import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_google_sheet(sheet_url):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('E:/python/pythonbot/bot-sheet-438808-de838a16ee8f.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_url(sheet_url).sheet1
    return sheet
