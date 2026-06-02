"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path
from sqlmodel import select

from src.db import engine, get_session
from src.models import Activity, Participant


app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# If DB hasn't been initialized, fallback to an empty dict (seed script will populate DB)



@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    from sqlmodel import Session
    with Session(engine) as session:
        results = session.exec(select(Activity)).all()
        out = {}
        for a in results:
            out[a.name] = {
                "description": a.description,
                "schedule": a.schedule,
                "max_participants": a.max_participants,
                "participants": [p.email for p in a.participants]
            }
        return out


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    from sqlmodel import Session
    with Session(engine) as session:
        statement = select(Activity).where(Activity.name == activity_name)
        result = session.exec(statement).first()
        if not result:
            raise HTTPException(status_code=404, detail="Activity not found")

        # check if already signed up
        for p in result.participants:
            if p.email == email:
                raise HTTPException(status_code=400, detail="Student is already signed up")

        # enforce max participants if set
        if result.max_participants and len(result.participants) >= result.max_participants:
            raise HTTPException(status_code=400, detail="Activity is full")

        new_p = Participant(email=email, activity_id=result.id)
        session.add(new_p)
        session.commit()
        return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str):
    """Unregister a student from an activity"""
    from sqlmodel import Session
    with Session(engine) as session:
        statement = select(Activity).where(Activity.name == activity_name)
        result = session.exec(statement).first()
        if not result:
            raise HTTPException(status_code=404, detail="Activity not found")

        # find participant
        participant = None
        for p in result.participants:
            if p.email == email:
                participant = p
                break

        if not participant:
            raise HTTPException(status_code=400, detail="Student is not signed up for this activity")

        session.delete(participant)
        session.commit()
        return {"message": f"Unregistered {email} from {activity_name}"}
