from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select

from models import Roster, StatLine, engine

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="Pens Roster App", version="1.0.0")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@app.get("/api/health")
def api_health() -> dict:
    return {"status": "ok"}


@app.get("/api/roster")
def api_roster(
    pos: Optional[str] = Query(default=None, description="Filter by position, e.g. C, RW, D, G"),
    limit: int = Query(default=100, ge=1, le=200),
) -> list[dict]:
    with Session(engine) as session:
        statement = select(Roster).order_by(Roster.player)
        if pos:
            statement = statement.where(Roster.pos == pos.upper())
        rows = session.exec(statement.limit(limit)).all()
    return [row.model_dump() for row in rows]


@app.get("/api/stats")
def api_stats(
    pos: Optional[str] = Query(default=None, description="Filter by position, e.g. C, RW, D, G"),
    limit: int = Query(default=100, ge=1, le=200),
) -> list[dict]:
    with Session(engine) as session:
        statement = select(StatLine).order_by(StatLine.player)
        if pos:
            statement = statement.where(StatLine.pos == pos.upper())
        rows = session.exec(statement.limit(limit)).all()
    return [row.model_dump() for row in rows]


@app.get("/api/top-scorers")
def api_top_scorers(limit: int = Query(default=10, ge=1, le=50)) -> list[dict]:
    with Session(engine) as session:
        rows = session.exec(
            select(StatLine)
            .where(StatLine.pos != "G")
            .order_by(StatLine.points.desc())
            .limit(limit)
        ).all()
    return [row.model_dump() for row in rows]


@app.get("/api/players/{player_name}")
def api_player(player_name: str) -> dict:
    with Session(engine) as session:
        roster = session.exec(select(Roster).where(Roster.player == player_name)).first()
        stats = session.exec(select(StatLine).where(StatLine.player == player_name)).first()

    if not roster and not stats:
        raise HTTPException(status_code=404, detail="Player not found")

    return {
        "player": player_name,
        "roster": roster.model_dump() if roster else None,
        "stats": stats.model_dump() if stats else None,
    }


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    with Session(engine) as session:
        top_scorers = session.exec(
            select(StatLine)
            .where(StatLine.pos != "G")
            .order_by(StatLine.points.desc())
            .limit(10)
        ).all()
        roster_count = len(session.exec(select(Roster)).all())

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "top_scorers": top_scorers,
            "roster_count": roster_count,
        },
    )


@app.get("/players", response_class=HTMLResponse)
def players_page(request: Request, pos: Optional[str] = None, q: Optional[str] = None):
    with Session(engine) as session:
        statement = select(Roster).order_by(Roster.player)
        if pos:
            statement = statement.where(Roster.pos == pos.upper())
        if q:
            statement = statement.where(Roster.player.contains(q))
        players = session.exec(statement).all()

    return templates.TemplateResponse(
        request=request,
        name="players.html",
        context={
            "players": players,
            "pos": pos or "",
            "q": q or "",
        },
    )


@app.get("/players/{player_name}", response_class=HTMLResponse)
def player_detail(request: Request, player_name: str):
    with Session(engine) as session:
        roster = session.exec(select(Roster).where(Roster.player == player_name)).first()
        stats = session.exec(select(StatLine).where(StatLine.player == player_name)).first()

    if not roster and not stats:
        raise HTTPException(status_code=404, detail="Player not found")

    return templates.TemplateResponse(
        request=request,
        name="player_detail.html",
        context={
            "player_name": player_name,
            "roster": roster,
            "stats": stats,
        },
    )
