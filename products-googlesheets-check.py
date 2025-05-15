import gspread
from google.oauth2.service_account import Credentials

creds_path = "google-sheets-api.json"
spreadsheet_name = "Fashion Products Clean"
sheet_name = "Cleaned Data"

# Autentikasi ke Google Sheets
scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
creds = Credentials.from_service_account_file(creds_path, scopes=scope)
client = gspread.authorize(creds)

# Buka spreadsheet dan worksheet
spreadsheet = client.open(spreadsheet_name)

try:
    worksheet = spreadsheet.worksheet(sheet_name)
    data = worksheet.get_all_values()
    
    if data:
        print(f"Menampilkan 5 baris pertama dari worksheet '{sheet_name}':")
        header = data[0]
        rows = data[1:6] 
        
        print(header)
        for row in rows:
            print(row)
    else:
        print(f"Worksheet '{sheet_name}' kosong.")
except gspread.exceptions.WorksheetNotFound:
    print(f"Worksheet '{sheet_name}' tidak ditemukan.")
