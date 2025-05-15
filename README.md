# ETL Pipeline - Fashion Products Data

Proyek ini merupakan implementasi pipeline ETL (Extract, Transform, Load) untuk mengumpulkan data produk fashion dari web scraping, membersihkan data, dan menyimpannya ke berbagai format termasuk CSV, Google Sheets, dan PostgreSQL.

---

## Struktur Proyek

├── main.py 
├── utils
│ ├── extract.py
│ ├── transform.py
│ └── load.py
├── tests # Unit testing
│ ├── test_extract.py
│ ├── test_transform.py
│ └── test_load.py
├── products_raw.csv # Data mentah hasil ekstraksi
├── products_clean.csv # Data bersih hasil transformasi
├── products_final.csv # Data final
├── google-sheets-api.json # Kredensial API Google Sheets
├── products-googlesheets-check.py 
├── products-postgreSQL-check.py
├── requirements.txt # Daftar dependencies Python
└── submission.txt # Penjelasan cara menjalankan

---


---

Penjelasan cara menjalankan:

ETL
-----
# Menjalankan skrip ETL
python main.py

Unit Test
---------
# Menjalankan Unit Test
python -m pytest tests

Test Coverage
-------------
# Melihat Test Coverage
coverage run -m pytest tests
coverage report

# Melihat Test Coverage Setiap Unit testing
coverage run -m pytest tests/test_extract.py
coverage report

coverage run -m pytest tests/test_transform.py
coverage report

coverage run -m pytest tests/test_load.py
coverage report

URL Google Sheets
-----------------
https://docs.google.com/spreadsheets/d/1E8ak4iI-mtbPX7Bzmj9tfn4h8llpj-b72SBoa8QSwow/edit?gid=0#gid=0

### Kontak
Cika Rahmannia Febrianti
cikarahmanniaa@gmail.com
