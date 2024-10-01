from sqlalchemy.orm import Session

import models, schemas

def get_subjects(db: Session):
    return db.query(models.Subjects).all()

def get_levels(db: Session):
    return db.query(models.Levels).all()

def get_recommended_targets(db: Session):
    return db.query(models.RecommendedTargets).all()

def get_facilities(db: Session, subject_ids: list[int], level_ids:list[int], recommended_target_ids:list[int]):
    return db.query(models.Facilities)\
        .filter(models.Facilities.subject_ids.in_(subject_ids))\
        .filter(models.Facilities.level_ids.in_(level_ids))\
        .filter(models.Facilities.recommended_target_ids.in_(recommended_target_ids))\
        .all()
