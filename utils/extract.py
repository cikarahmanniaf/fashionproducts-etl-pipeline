import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import logging
import time
import re

logging.basicConfig(level=logging.INFO)

def parse_product(product):
    title = product.find("h3", class_="product-title").get_text(strip=True)

    # Menangani dua kemungkinan harga
    price_tag = product.find("span", class_="price")
    if not price_tag:
        price_tag = product.find("p", class_="price")
    price = price_tag.get_text(strip=True) if price_tag else None

    # Ambil semua <p> untuk informasi tambahan
    p_tags = product.find_all("p")
    rating, colors, size, gender = [None] * 4

    for p in p_tags:
        text = p.get_text(strip=True)
        if "Rating" in text:
            rating = text  
        elif "Colors" in text:
            colors = text
        elif "Size:" in text:
            size = text  
        elif "Gender:" in text:
            gender = text 

    return {
        "title": title,
        "price": price,
        "rating": rating,
        "colors": colors,
        "size": size,
        "gender": gender,
        "timestamp": datetime.now().isoformat()
    }

def extract_data(page_limit=50):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    all_data = []

    for page in range(1, page_limit + 1):
        if page == 1:
            url = "https://fashion-studio.dicoding.dev/"
        else:
            url = f"https://fashion-studio.dicoding.dev/page{page}"
        try:
            logging.info(f"Scraping halaman {page} dari URL: {url}")
            response = requests.get(url, headers=headers)

            if response.status_code != 200:
                raise Exception(f"Failed to fetch page {page}: {response.status_code}")

            soup = BeautifulSoup(response.text, 'html.parser')
            products = soup.find_all("div", class_="collection-card")

            for product in products:
                data = parse_product(product)
                all_data.append(data)

            time.sleep(0.3)  # Jeda antar request
        except Exception as e:
            logging.error(f"Error di halaman {page}: {e}")

    df = pd.DataFrame(all_data)
    logging.info(f"Scraping selesai. Total produk: {len(df)}")

    # Simpan ke file
    df.to_csv("products_raw.csv", index=False)
    return df

if __name__ == "__main__":
    df = extract_data()
    print(df.head())
