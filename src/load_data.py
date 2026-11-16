from pathlib import Path
import pandas as pd

RAW_DIR = Path("data/raw")
OUT_FILE = Path("data/processed/matches.csv")
COLUMNS = ["Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG", "FTR"]


def load_season(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, encoding="latin-1")
    df = df[COLUMNS].dropna()
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, format="mixed")
    df["season"] = path.stem.split("_")[1]
    return df


def main() -> None:
    frames = [load_season(p) for p in sorted(RAW_DIR.glob("*.csv"))]
    matches = pd.concat(frames, ignore_index=True)
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    matches.to_csv(OUT_FILE, index=False)
    print(f"{len(matches)} meczów, {len(frames)} sezonów")


if __name__ == "__main__":
    main()