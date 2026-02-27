import csv
from pathlib import Path

from sqlmodel import SQLModel, create_engine, Session

from models import Roster, StatLine

DB_PATH = Path("penguins.db")
ROSTER_CSV = Path("roster.csv")
STATS_CSV = Path("stats.csv")


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
                roster = Roster(
                    player=row.get("player"),
                    number=int(row["number"]) if row.get("number") else None,
                    pos=row.get("pos") or None,
                    sh=row.get("sh"),
                    ht=row.get("ht"),
                    wt=int(row["wt"]) if row.get("wt") else None,
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
                # Helper converters
                def to_int(val):
                    return int(val) if val and val.isdigit() else None

                def to_float(val):
                    try:
                        return float(val)
                    except (TypeError, ValueError):
                        return None

                stat = StatLine(
                    player=row.get("player"),
                    pos=row.get("pos") or None,
                    gp=to_int(row.get("gp")),
                    goals=to_int(row.get("goals")),
                    assists=to_int(row.get("assists")),
                    points=to_int(row.get("points")),
                    plus_minus=row.get("plus_minus"),
                    pim=to_int(row.get("pim")),
                    ppg=to_int(row.get("ppg")),
                    shg=to_int(row.get("shg")),
                    gwg=to_int(row.get("gwg")),
                    otg=to_int(row.get("otg")),
                    s=to_int(row.get("s")),
                    s_pct=to_float(row.get("s_pct")),
                    toi_per_game=row.get("toi_per_game"),
                    sft_per_game=row.get("sft_per_game"),
                    fo_pct=row.get("fo_pct"),
                    gs=to_int(row.get("gs")),
                    w=to_int(row.get("w")),
                    l=to_int(row.get("l")),
                    t=to_int(row.get("t")),
                    ot=to_int(row.get("ot")),
                    gaa=to_float(row.get("gaa")),
                    sv_pct=to_float(row.get("sv_pct")),
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
