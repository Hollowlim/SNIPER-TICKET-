"""Local-only mock event API. No ticketing-platform automation."""
import os
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import Boolean, Integer, String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

engine = create_engine(os.getenv("DATABASE_URL", "sqlite:///./yeng.db"))
class Base(DeclarativeBase):
    pass
class Event(Base):
    __tablename__ = "events"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    subtitle: Mapped[str] = mapped_column(String(200))
    venue: Mapped[str] = mapped_column(String(200))
    date: Mapped[str] = mapped_column(String(50))
    genre: Mapped[str] = mapped_column(String(50))
    theme: Mapped[str] = mapped_column(String(50))
    price: Mapped[int] = mapped_column(Integer)
    watching: Mapped[bool] = mapped_column(Boolean, default=False)
    updated_at: Mapped[str] = mapped_column(String(50))

SEEDS = [
    ("AURORA", "WHAT HAPPENED TO THE EARTH?", "Zepp Kuala Lumpur", "2027-03-14T20:00:00+08:00", "Concert", "aurora", 288),
    ("THE MIDNIGHT", "SHADOWS & NEON · LIVE IN KL", "Mega Star Arena", "2027-04-18T20:30:00+08:00", "Concert", "midnight", 258),
    ("LA LA LAND", "IN CONCERT", "Dewan Filharmonik PETRONAS", "2027-05-22T19:30:00+08:00", "Arts & Theatre", "lalaland", 198),
    ("NIKI", "BUZZ WORLD TOUR", "Axiata Arena, Bukit Jalil", "2027-06-12T20:00:00+08:00", "Concert", "niki", 328),
    ("AFTER HOURS", "KUALA LUMPUR COMEDY CLUB", "The Joke Factory", "2027-03-27T21:00:00+08:00", "Comedy", "comedy", 88),
    ("CITY IN MOTION", "A WEEKEND OF SOUND & CULTURE", "KL Base, Sungai Besi", "2027-07-10T16:00:00+08:00", "Festival", "festival", 188),
]
@asynccontextmanager
async def lifespan(app):
    Base.metadata.create_all(engine)
    with Session(engine) as db:
        if not db.scalar(select(Event.id).limit(1)):
            for title, subtitle, venue, date, genre, theme, price in SEEDS:
                db.add(Event(title=title, subtitle=subtitle, venue=venue, date=date, genre=genre, theme=theme, price=price, updated_at=datetime.now(timezone.utc).isoformat()))
            db.commit()
    yield
app = FastAPI(title="YENG Ticket Sniper", lifespan=lifespan)

def serialize(event):
    return {"id": event.id, "title": event.title, "subtitle": event.subtitle, "venue": event.venue, "date": event.date, "genre": event.genre, "theme": event.theme, "price": event.price, "watching": event.watching, "source": "Mock adapter", "updated_at": event.updated_at, "sale_date": None, "official_url": None, "categories": [{"name": name, "price": event.price + i * 100, "publication": "mock", "availability": "unknown"} for i, name in enumerate(["PS2", "PS1", "VIP"])]}
@app.get("/api/health")
def health():
    with Session(engine) as db:
        db.execute(select(Event.id).limit(1))
    return {"status": "ok", "mode": "mock"}
@app.get("/api/events")
def events(q: str = "", genre: str = ""):
    with Session(engine) as db:
        records = db.scalars(select(Event).order_by(Event.id)).all()
        return [serialize(e) for e in records if q.casefold() in (e.title + " " + e.venue).casefold() and (not genre or e.genre == genre)]
@app.get("/api/events/{event_id}")
def detail(event_id: int):
    with Session(engine) as db:
        event = db.get(Event, event_id)
        if not event:
            raise HTTPException(404, "Event not found")
        return serialize(event)
class WatchUpdate(BaseModel):
    watching: bool
@app.put("/api/events/{event_id}/watch")
def watch(event_id: int, update: WatchUpdate):
    with Session(engine) as db:
        event = db.get(Event, event_id)
        if not event:
            raise HTTPException(404, "Event not found")
        event.watching = update.watching
        db.commit()
        return serialize(event)
