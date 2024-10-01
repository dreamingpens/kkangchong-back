from sqlalchemy.orm import Session

from . import models, schemas

def get_subjects(db: Session):
    return db.query(models.Subjects).all()

def get_levels(db: Session):
    return db.query(models.Levels).all()

def get_disability_types(db: Session):
    return db.query(models.DisabilityTypes).all()

def get_facilities(db: Session, subject_ids: list[int], level_ids:list[int], disability_type_ids:list[int]):
    return db.query(models.Facilities)\
        .filter(models.Facilities.subject_ids.in_(subject_ids))\
        .filter(models.Facilities.level_ids.in_(level_ids))\
        .filter(models.Facilities.disability_type_ids.in_(disability_type_ids))\
        .all()
