import pytest
import pandas as pd
import tempfile
import sys
import os
from unittest.mock import patch, MagicMock
from gspread.exceptions import WorksheetNotFound, APIError  

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import load

# Fixture: DataFrame contoh untuk pengujian
@pytest.fixture
def contoh_df():
    return pd.DataFrame({
        'title': ['Product A'],
        'price': [100000],
        'rating': [4.5],
        'colors': [3],
        'size': ['M'],
        'gender': ['Men'],
        'timestamp': [pd.Timestamp('2024-01-01')]
    })

# Pengujian fungsi simpan_ke_csv
def test_simpan_ke_csv(contoh_df):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmpfile:
        nama_file = tmpfile.name
    try:
        load.simpan_ke_csv(contoh_df, nama_file)
        assert os.path.exists(nama_file)
        df_hasil = pd.read_csv(nama_file)
        assert df_hasil.shape == contoh_df.shape
    finally:
        os.remove(nama_file)

# Pengujian fungsi simpan_ke_google_sheets dengan mock spesifik
@patch("utils.load.Credentials")
@patch("utils.load.gspread.authorize")
@patch("utils.load.gspread.exceptions.WorksheetNotFound", new=WorksheetNotFound)
def test_simpan_ke_google_sheets(mock_authorize, mock_credentials, contoh_df):
    mock_client = MagicMock()
    mock_spreadsheet = MagicMock()
    mock_worksheet = MagicMock()

    # Setup mock
    mock_authorize.return_value = mock_client
    mock_client.open.return_value = mock_spreadsheet
    mock_spreadsheet.worksheet.side_effect = WorksheetNotFound("Sheet tidak ditemukan")
    mock_spreadsheet.add_worksheet.return_value = mock_worksheet

    # Menjalankan fungsi yang diuji
    load.simpan_ke_google_sheets(contoh_df, path_kredensial="dummy-path.json")

    # Verifikasi
    mock_authorize.assert_called_once()
    mock_client.open.assert_called_once()
    mock_spreadsheet.worksheet.assert_called_once_with("Cleaned Data")
    mock_spreadsheet.add_worksheet.assert_called_once_with(
        title="Cleaned Data",
        rows=str(len(contoh_df) + 1),
        cols=str(len(contoh_df.columns))
    )
    mock_worksheet.update.assert_called_once_with(
        [contoh_df.columns.tolist()] + contoh_df.values.tolist()
    )

# Pengujian fungsi simpan_ke_postgres dengan mock
@patch("utils.load.create_engine")
@patch("pandas.DataFrame.to_sql")
def test_simpan_ke_postgres(mock_to_sql, mock_create_engine, contoh_df):
    mock_engine = MagicMock()
    mock_create_engine.return_value = mock_engine

    load.simpan_ke_postgres(contoh_df, "tabel_uji", "postgresql://user:pass@localhost:5432/db")

    mock_create_engine.assert_called_once()
    mock_to_sql.assert_called_once_with(
        "tabel_uji",
        mock_engine,
        if_exists='replace',
        index=False
    )


# --------- Test Coverage ---------

# PS D:\Coding Camp 2025 DBS Foundation (Dicoding)\Proyek 5_ETL Pipeline> coverage run -m pytest tests/test_load.py
# >> coverage report
# ======================================= test session starts ========================================
# platform win32 -- Python 3.12.4, pytest-8.3.5, pluggy-1.5.0
# rootdir: D:\Coding Camp 2025 DBS Foundation (Dicoding)\Proyek 5_ETL Pipeline
# collected 3 items                                                                                   
# 
# tests\test_load.py ...                                                                        [100%]
# 
# ======================================== 3 passed in 7.34s ========================================= 
# Name                 Stmts   Miss  Cover
# ----------------------------------------
# tests\test_load.py      46      0   100%
# utils\load.py           51     19    63%
# ----------------------------------------
# TOTAL                   97     19    80%
