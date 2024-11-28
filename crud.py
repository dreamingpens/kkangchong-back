from sqlalchemy.orm import Session

import models, schemas

def get_clubs(db: Session, subject: str):
    clubs = db.query(models.Clubs).filter(models.Clubs.subject == subject).all()

    return [
        {   
            "id": club.id,
            "location": club.location,
            "club_name": club.club_name,
            "active_time": club.active_time,
            "subject": club.subject,
            "other_objects": club.other_objects or "",
            "disability_type": club.disability_type,
            "permission_date": club.permission_date
        }
        for club in clubs
    ]