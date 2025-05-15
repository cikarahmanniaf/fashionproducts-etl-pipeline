from sqlalchemy import create_engine
import pandas as pd

# URL database PostgreSQL
postgres_url = "postgresql://postgres:14022002@localhost:5432/etl_db"
engine = create_engine(postgres_url)

# Query untuk mengambil data dari tabel products
query = "SELECT * FROM products LIMIT 10"
df = pd.read_sql(query, engine)

print(df)
