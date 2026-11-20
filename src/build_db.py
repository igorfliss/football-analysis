import sqlite3
from pathlib import Path

import pandas as pd

CSV_FILE = Path("data/processed/matches_clean.csv")
DB_FILE = Path("data/football.db")


def main() -> None:
    df = pd.read_csv(CSV_FILE, parse_dates=["match_date"])
    df["match_date"] = df["match_date"].dt.strftime("%Y-%m-%d")

    with sqlite3.connect(DB_FILE) as conn:
        df.to_sql("matches", conn, if_exists="replace", index=False)
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_matches_league_season "
            "ON matches (league, season)"
        )
    print(f"Zapisano {len(df)} wierszy do tabeli matches w {DB_FILE}")


if __name__ == "__main__":
    main()