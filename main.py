from utils.extract import extract_data
from utils.transform import transform_data
from utils.load import simpan_ke_csv, simpan_ke_google_sheets, simpan_ke_postgres

from datetime import datetime
import logging

def main():
    logging.basicConfig(level=logging.INFO)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    logging.info("Mulai proses ekstraksi data...")
    df_raw = extract_data(page_limit=50)  

    logging.info("Mulai proses transformasi data...")
    input_path = "products_raw.csv"
    output_path = f"products_clean_{timestamp}.csv"
    df_clean = transform_data(input_path=input_path, output_path=output_path)

    if df_clean.empty:
        logging.warning("Data hasil transformasi kosong. Proses selesai tanpa penyimpanan.")
        return

    logging.info("Menyimpan data ke berbagai format...")
    simpan_ke_csv(df_clean, nama_file=f"products_final_{timestamp}.csv")
    simpan_ke_google_sheets(df_clean, path_kredensial="google-sheets-api.json")

    postgres_url = "postgresql://postgres:14022002@localhost:5432/etl_db"
    simpan_ke_postgres(df_clean, nama_tabel="products", db_url=postgres_url)

if __name__ == "__main__":
    main()
