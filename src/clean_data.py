from pathlib import Path
import pandas as pd 
import numpy as np

RAW_DIR = Path("data/raw")
OUT_FILE = Path("data/processed/matches_clean.csv")

LEAGUES = { "E0": "Premier League",
    "SP1": "La Liga",
    "I1": "Serie A",
    "D1": "Bundesliga",
    "F1": "Ligue 1",
    }
RENAME = {
    "Date": "match_date",
    "HomeTeam": "home_team",
    "AwayTeam": "away_team",
    "FTHG": "home_goals",
    "FTAG": "away_goals",
    "FTR": "result",
    "HTHG": "ht_home_goals",
    "HTAG": "ht_away_goals",
    "HS": "home_shots",
    "AS": "away_shots",
    "HST": "home_shots_on_target",
    "AST": "away_shots_on_target",
    "HF": "home_fouls",
    "AF": "away_fouls",
    "HC": "home_corners",
    "AC": "away_corners",
    "HY": "home_yellow",
    "AY": "away_yellow",
    "HR": "home_red",
    "AR": "away_red",
    "B365H": "odds_home",
    "B365D": "odds_draw",
    "B365A": "odds_away",
}
CORE = ["match_date", "home_team", "away_team", "home_goals", "away_goals", "result"]

def load_season(path: Path) -> pd.DataFrame:
    code, season = path.stem.split("_")
    df = pd.read_csv(path, encoding="latin-1")
    df = df.rename(columns=RENAME)
    df = df.reindex(columns=list(RENAME.values()))
    df = df.dropna(subset=CORE)
    df["match_date"] = pd.to_datetime(df["match_date"], dayfirst=True, format="mixed")
    df["league"] = LEAGUES[code]
    df["season"] = f"20{season[:2]}/{season[2:]}"  # zamiana nazwy sezonu na bardziej czytelny format: 1516 -> 2015/16
    return df

def clean(matches: pd.DataFrame) -> pd.DataFrame:
    # usuwa zbędne spacje z nazw drużyn
    for col in ["home_team", "away_team"]:
        matches[col] = matches[col].str.strip()

    # zamiana kolumn z golami na typ int
    matches[["home_goals", "away_goals"]] = matches[["home_goals", "away_goals"]].astype(int)

    # jakby były duplikaty, to zostawiamy tylko jeden wiersz
    before = len(matches)
    matches = matches.drop_duplicates(subset=["match_date", "home_team", "away_team"])
    print(f"Usunięte duplikaty: {before - len(matches)}")

    # sprawdzam czy wynik (H/D/A) zgadza się z golami
    expected = np.select(
        [matches["home_goals"] > matches["away_goals"],
         matches["home_goals"] < matches["away_goals"]],
        ["H", "A"],
        default="D",
    )
    bad = matches["result"] != expected
    print(f"Wiersze z niezgodnym wynikiem (usunięte): {bad.sum()}")
    matches = matches[~bad]

    #numer meczu
    matches = matches.sort_values(["match_date", "league", "home_team"]).reset_index(drop=True)
    matches.insert(0, "match_id", matches.index + 1)
    return matches


def main() -> None:
    frames = [
        load_season(p)
        for p in sorted(RAW_DIR.glob("*.csv"))
        if p.stem.split("_")[1]
    ]
    matches = clean(pd.concat(frames, ignore_index=True))

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    matches.to_csv(OUT_FILE, index=False)

    print(f"\nZapisano {len(matches)} meczów z {len(frames)} plików")
    print("\nOdsetek braków (%) w każdej kolumnie:")
    print((matches.isna().mean() * 100).round(1).to_string())


if __name__ == "__main__":
    main()