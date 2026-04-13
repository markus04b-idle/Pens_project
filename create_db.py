import csv
from pathlib import Path

from sqlmodel import SQLModel, create_engine, Session

from models import Roster, StatLine

DB_PATH = Path("penguins.db")
ROSTER_CSV = Path("roster.csv")
STATS_CSV = Path("stats.csv")


def normalize_row(row: dict) -> dict:
    normalized = {}
    for key, value in row.items():
        cleaned_key = (key or "").strip().lower()
        normalized[cleaned_key] = value.strip() if isinstance(value, str) else value
    return normalized


def to_int(value):
    if value is None:
        return None
    text = str(value).strip()
    if not text or text in {"-", "--"}:
        return None
    try:
        return int(float(text))
    except ValueError:
        return None


def to_float(value):
    if value is None:
        return None
    text = str(value).strip()
    if not text or text in {"-", "--"}:
        return None
    if text.startswith("."):
        text = f"0{text}"
    try:
        return float(text)
    except ValueError:
        return None


def create_database(engine):
    """Drop and recreate the database schema."""
    # remove existing file if present for a clean start
    if DB_PATH.exists():
        DB_PATH.unlink()
    SQLModel.metadata.create_all(engine)


def load_roster(engine):
    """Read roster.csv and insert rows into the Roster table."""
    with open(ROSTER_CSV, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        with Session(engine) as session:
            for row in reader:
                row = normalize_row(row)
                roster = Roster(
                    player=row.get("player"),
                    number=to_int(row.get("#")),
                    pos=row.get("pos") or None,
                    sh=row.get("sh"),
                    ht=row.get("ht"),
                    wt=to_int(row.get("wt")),
                    born=row.get("born"),
                    birthplace=row.get("birthplace"),
                )
                session.add(roster)
            session.commit()


def load_stats(engine):
    """Read stats.csv and insert rows into the StatLine table."""
    with open(STATS_CSV, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        with Session(engine) as session:
            for row in reader:
                row = normalize_row(row)
                is_goalie = row.get("pos") == "G"

                stat = StatLine(
                    player=row.get("player"),
                    pos=row.get("pos") or None,
                    gp=to_int(row.get("gp")),
                    goals=to_int(row.get("g")) if not is_goalie else None,
                    assists=to_int(row.get("a")) if not is_goalie else None,
                    points=to_int(row.get("p")) if not is_goalie else None,
                    plus_minus=row.get("+/-"),
                    pim=to_int(row.get("pim")),
                    ppg=to_int(row.get("ppg")),
                    shg=to_int(row.get("shg")),
                    gwg=to_int(row.get("gwg")),
                    otg=to_int(row.get("otg")),
                    s=to_int(row.get("s")),
                    s_pct=to_float(row.get("s%")),
                    toi_per_game=row.get("toi/g"),
                    sft_per_game=row.get("sft/g"),
                    fo_pct=row.get("fo%"),
                    gs=to_int(row.get("gs")),
                    w=to_int(row.get("w")),
                    l=to_int(row.get("l")),
                    t=to_int(row.get("t")),
                    ot=to_int(row.get("ot")),
                    gaa=to_float(row.get("gaa")),
                    sv_pct=to_float(row.get("sv%")),
                    sa=to_int(row.get("sa")),
                    sv=to_int(row.get("sv")),
                    ga=to_int(row.get("ga")),
                    so=to_int(row.get("so")),
                )
                session.add(stat)
            session.commit()


if __name__ == "__main__":
    engine = create_engine(f"sqlite:///{DB_PATH}")
    print("creating schema...")
    create_database(engine)
    print("loading roster...")
    load_roster(engine)
    print("loading stats...")
    load_stats(engine)
    print("done")
