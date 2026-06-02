from sqlmodel import SQLModel
from src.db import engine
from src.models import Activity, Participant

def seed():
    SQLModel.metadata.create_all(engine)

    activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        }
    }

    from sqlmodel import Session
    with Session(engine) as session:
        for name, data in activities.items():
            act = Activity(name=name, description=data.get("description"),
                           schedule=data.get("schedule"),
                           max_participants=data.get("max_participants"))
            session.add(act)
            session.commit()
            session.refresh(act)
            for email in data.get("participants", []):
                p = Participant(email=email, activity_id=act.id)
                session.add(p)
        session.commit()

if __name__ == "__main__":
    seed()
