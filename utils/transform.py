import pandas as pd
import logging
import re

logging.basicConfig(level=logging.INFO)

def clean_price(price_str):
    try:
        if price_str == "Price Unavailable" or not price_str.strip():
            return None  # Return None jika price tidak tersedia atau null
        usd = float(price_str.replace('$', '').replace(',', ''))
        return usd * 16000
    except Exception as e:
        logging.warning(f"Gagal parsing price: {price_str} | {e}")
        return None

def clean_rating(rating_str):
    try:
        match = re.search(r'(\d+(\.\d+)?)\s*/\s*5', rating_str)
        return float(match.group(1)) if match else None
    except Exception as e:
        logging.warning(f"Gagal parsing rating: {rating_str} | {e}")
        return None

def clean_colors(colors_str):
    try:
        match = re.search(r'(\d+)', colors_str)
        return int(match.group(1)) if match else None
    except Exception as e:
        logging.warning(f"Gagal parsing colors: {colors_str} | {e}")
        return None

def clean_size(size_str):
    try:
        return size_str.replace('Size:', '').strip() if isinstance(size_str, str) else None
    except Exception as e:
        logging.warning(f"Gagal parsing size: {size_str} | {e}")
        return None

def clean_gender(gender_str):
    try:
        return gender_str.replace('Gender:', '').strip() if isinstance(gender_str, str) else None
    except Exception as e:
        logging.warning(f"Gagal parsing gender: {gender_str} | {e}")
        return None

def transform_data(input_path="products_raw.csv", output_path="products_clean.csv"):
    try:
        df = pd.read_csv(input_path)
        logging.info("Mulai transformasi data...")

        # Cleaning
        df['price'] = df['price'].apply(clean_price)
        df['rating'] = df['rating'].apply(clean_rating)
        df['colors'] = df['colors'].apply(clean_colors)
        df['size'] = df['size'].apply(clean_size)
        df['gender'] = df['gender'].apply(clean_gender)

        # Convert timestamp
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

        invalid_timestamps = df['timestamp'].isna().sum()
        if invalid_timestamps > 0:
            logging.warning(f"{invalid_timestamps} invalid timestamps found and coerced to NaT.")

        # Drop data invalid
        df = df[df['title'] != "Unknown Product"]

        # Drop duplicates dan null
        df = df.drop_duplicates()
        df = df.dropna()

        df.to_csv(output_path, index=False)
        logging.info(f"Data berhasil disimpan: {output_path}, total baris: {len(df)}")
        return df

    except Exception as e:
        logging.error(f"Terjadi kesalahan saat transformasi: {e}")
        return pd.DataFrame()

if __name__ == "__main__":
    transform_data()
