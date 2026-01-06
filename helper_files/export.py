import os
import pandas as pd
from db_config_1 import create_connection

# -------------------------
# CONFIG
# -------------------------
EXPORT_DIR = "data_exports"
TABLES = [
    "fixtures_current_season"
]

os.makedirs(EXPORT_DIR, exist_ok=True)

conn = create_connection()

for table in TABLES:
    print(f"📤 Exporting {table} ...")

    df = pd.read_sql(f"SELECT * FROM {table}", conn)

    output_path = os.path.join(EXPORT_DIR, f"{table}.csv")
    df.to_csv(output_path, index=False)

    print(f"✅ Saved {output_path} ({len(df)} rows)")

conn.close()

print("🎯 All tables exported successfully.")
