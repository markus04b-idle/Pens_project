from sqlmodel import SQLModel, Field, create_engine
from typing import Optional
from pathlib import Path

# small shared engine so other modules can import it
DB_PATH = Path("penguins.db")
engine = create_engine(f"sqlite:///{DB_PATH}")


class Roster(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    player: str
    number: Optional[int]
    pos: Optional[str]
    sh: Optional[str]  # shoots
    ht: Optional[str]
    wt: Optional[int]
    born: Optional[str]
    birthplace: Optional[str]


class StatLine(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    player: str
    pos: Optional[str]
    gp: Optional[int]
    goals: Optional[int]
    assists: Optional[int]
    points: Optional[int]
    plus_minus: Optional[str]
    pim: Optional[int]
    ppg: Optional[int]
    shg: Optional[int]
    gwg: Optional[int]
    otg: Optional[int]
    s: Optional[int]
    s_pct: Optional[float]
    toi_per_game: Optional[str]
    sft_per_game: Optional[str]
    fo_pct: Optional[str]
    # goalie-specific fields follow; these remain null for skaters
    gs: Optional[int]
    w: Optional[int]
    l: Optional[int]
    t: Optional[int]
    ot: Optional[int]
    gaa: Optional[float]
    sv_pct: Optional[float]
    sa: Optional[int]
    sv: Optional[int]
    ga: Optional[int]
    so: Optional[int]

# Provide aliases expected by older code (`read.py` imports `Bio` and `Stats`)
Bio = Roster
Stats = StatLine
