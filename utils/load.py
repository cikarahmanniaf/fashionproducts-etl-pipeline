import pandas as pd
import logging
import gspread
from google.oauth2.service_account import Credentials
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from gspread.exceptions import WorksheetNotFound, APIError

# Konfigurasi logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Fungsi 1: Simpan ke CSV
def simpan_ke_csv(df, nama_file="products_final.csv"):
    try:
        df.to_csv(nama_file, index=False)
        logging.info(f"Data berhasil disimpan ke CSV: {nama_file}")
    except Exception as e:
        logging.error(f"Gagal menyimpan ke CSV: {e}")

# Fungsi 2: Simpan ke Google Sheets
def simpan_ke_google_sheets(df, path_kredensial="google-sheets-api.json",
                             nama_spreadsheet="Fashion Products Clean",
                             nama_sheet="Cleaned Data"):
    try:
        df['timestamp'] = df['timestamp'].astype(str)

        scope = ['https://www.googleapis.com/auth/spreadsheets',
                 'https://www.googleapis.com/auth/drive']
        creds = Credentials.from_service_account_file(path_kredensial, scopes=scope)
        client = gspread.authorize(creds)
        spreadsheet = client.open(nama_spreadsheet)

        try:
            worksheet = spreadsheet.worksheet(nama_sheet)
            worksheet.clear()
            logging.info(f"Worksheet '{nama_sheet}' sudah ada, memperbarui isinya.")
        except WorksheetNotFound:  
            worksheet = spreadsheet.add_worksheet(title=nama_sheet,
                                                  rows=str(len(df) + 1),
                                                  cols=str(len(df.columns)))
            logging.info(f"Worksheet '{nama_sheet}' berhasil dibuat.")

        worksheet.update([df.columns.tolist()] + df.values.tolist())
        logging.info(f"Data berhasil disimpan ke Google Sheets: {nama_spreadsheet} - {nama_sheet}")
    except APIError as e:  
        logging.error(f"Terjadi kesalahan pada Google Sheets API: {e}")
    except Exception as e:
        logging.error(f"Gagal menyimpan ke Google Sheets: {e}")

# Fungsi 3: Simpan ke PostgreSQL
def simpan_ke_postgres(df, nama_tabel, db_url):
    try:
        engine = create_engine(db_url)
        df.to_sql(nama_tabel, engine, if_exists='replace', index=False)
        logging.info(f"Data berhasil disimpan ke PostgreSQL: {nama_tabel}")
    except SQLAlchemyError as e:
        logging.error(f"Kesalahan database: {e}")
    except Exception as e:
        logging.error(f"Gagal menyimpan ke PostgreSQL: {e}")

if __name__ == "__main__":
    try:
        df = pd.read_csv("products_clean.csv")

        # Simpan ke berbagai format
        simpan_ke_csv(df)
        simpan_ke_google_sheets(df)
        simpan_ke_postgres(df, nama_tabel="products", db_url="postgresql://postgres:14022002@localhost:5432/etl_db")

    except Exception as e:
        logging.error(f"Terjadi kesalahan saat menjalankan proses load: {e}")
