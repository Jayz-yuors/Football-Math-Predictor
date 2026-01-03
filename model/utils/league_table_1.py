"""
league_table_1.py

Purpose:
--------
Manual test runner for league_table.py
"""

from .league_table import fetch_league_table

if __name__ == "__main__":
    df = fetch_league_table("PL", 2025)
    print(df)
    print("\nRows:", len(df))
    print("\nColumns:", df.columns.tolist())
