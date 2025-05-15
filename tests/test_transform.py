import unittest
import pandas as pd
import sys
import os
import logging
from tempfile import NamedTemporaryFile

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import transform

logging.basicConfig(level=logging.INFO)

class TestTransformFunctions(unittest.TestCase):

    def test_clean_price(self):
        self.assertEqual(transform.clean_price("$1,234.56"), 1234.56 * 16000)
        self.assertEqual(transform.clean_price("Price Unavailable"), None)
        self.assertEqual(transform.clean_price(""), None)
        self.assertEqual(transform.clean_price(None), None)

    def test_clean_rating(self):
        self.assertEqual(transform.clean_rating("4.5 / 5"), 4.5)
        self.assertEqual(transform.clean_rating("Rating: 3 / 5"), 3.0)
        self.assertEqual(transform.clean_rating("No rating"), None)

    def test_clean_colors(self):
        self.assertEqual(transform.clean_colors("Colors Available: 12"), 12)
        self.assertEqual(transform.clean_colors("No colors"), None)

    def test_clean_size(self):
        self.assertEqual(transform.clean_size("Size: L"), "L")
        self.assertEqual(transform.clean_size(None), None)

    def test_clean_gender(self):
        self.assertEqual(transform.clean_gender("Gender: Men"), "Men")
        self.assertEqual(transform.clean_gender(None), None)

    def test_transform_data(self):
        # Membuat DataFrame dummy
        dummy_data = pd.DataFrame({
            "title": ["Test Product", "Unknown Product"],
            "price": ["$1,000.00", "Price Unavailable"],
            "rating": ["4.0 / 5", "Rating: 5 / 5"],
            "colors": ["Colors: 5", "Colors: 2"],
            "size": ["Size: M", "Size: L"],
            "gender": ["Gender: Women", "Gender: Men"],
            "timestamp": ["2024-05-12T10:00:00", "invalid"]
        })

        with NamedTemporaryFile(delete=False, suffix=".csv") as input_tmp, \
             NamedTemporaryFile(delete=False, suffix=".csv") as output_tmp:

            dummy_data.to_csv(input_tmp.name, index=False)
            df_result = transform.transform_data(input_path=input_tmp.name, output_path=output_tmp.name)

            # Hasil
            self.assertEqual(len(df_result), 1)
            self.assertIn("price", df_result.columns)
            self.assertTrue(pd.api.types.is_datetime64_any_dtype(df_result["timestamp"]))

        # Bersihkan file
        os.remove(input_tmp.name)
        os.remove(output_tmp.name)

if __name__ == "__main__":
    unittest.main()


# ------ Test Coverage --------

# PS D:\Coding Camp 2025 DBS Foundation (Dicoding)\Proyek 5_ETL Pipeline> coverage run -m pytest tests/test_transform.py
# >> coverage report
# =========================================== test session starts ===========================================
# platform win32 -- Python 3.12.4, pytest-8.3.5, pluggy-1.5.0
# rootdir: D:\Coding Camp 2025 DBS Foundation (Dicoding)\Proyek 5_ETL Pipeline
# collected 6 items
# 
# tests\test_transform.py ......                                                                       [100%]
# 
# ============================================ 6 passed in 3.23s ============================================
# Name                      Stmts   Miss  Cover
# ---------------------------------------------
# tests\test_transform.py      40      1    98%
# utils\transform.py           63     16    75%
# ---------------------------------------------
# TOTAL                       103     17    83%

