import shutil
import pytest
import pandas as pd
import sys
import os
from unittest.mock import patch, Mock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.extract import extract_data

@patch("utils.extract.requests.get")
def test_extract_data_mock(mock_get):
    output_filename = "products_raw.csv"

    # Backup jika file sudah ada
    if os.path.exists(output_filename):
        shutil.copy(output_filename, output_filename + ".backup")

    # HTML palsu
    html = '''
    <div class="collection-card">
        <h3 class="product-title">Casual Shirt</h3>
        <span class="price">$25</span>
        <p>Rating: 4.5 / 5</p>
        <p>Colors: 3 Colors</p>
        <p>Size: M</p>
        <p>Gender: Men</p>
    </div>
    '''

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = html
    mock_get.return_value = mock_response

    df = extract_data(page_limit=1)

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1
    assert df.iloc[0]["title"] == "Casual Shirt"
    assert df.iloc[0]["price"] == "$25"
    assert os.path.exists(output_filename)

    # Membersihkan file hasil mock
    os.remove(output_filename)

    # Restore backup jika ada
    if os.path.exists(output_filename + ".backup"):
        shutil.move(output_filename + ".backup", output_filename)


# -------- Test Coverage ----------

# PS D:\Coding Camp 2025 DBS Foundation (Dicoding)\Proyek 5_ETL Pipeline> coverage run -m pytest tests/test_extract.py
# >> coverage report
# ======================================= test session starts ========================================
# platform win32 -- Python 3.12.4, pytest-8.3.5, pluggy-1.5.0
# rootdir: D:\Coding Camp 2025 DBS Foundation (Dicoding)\Proyek 5_ETL Pipeline
# collected 1 item                                                                                    

# tests\test_extract.py .                                                                       [100%]

# ======================================== 1 passed in 7.78s ========================================= 
# Name                    Stmts   Miss  Cover
# -------------------------------------------
# tests\test_extract.py      27      0   100%
# utils\extract.py           54      7    87%
# -------------------------------------------
# TOTAL                      81      7    91%


