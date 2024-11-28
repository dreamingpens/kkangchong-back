from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Clubs
from datetime import datetime, date

session = SessionLocal()

Base.metadata.create_all(bind=engine)

import pandas as pd

# 클럽 데이터 로드
club_df = pd.read_excel('data/club_data.xlsx')

# 새로운 클럽 객체 생성
new_clubs = []
for _, row in club_df.iterrows():
    club = Clubs(
        location=row['지역'],
        club_name=row['클럽명'], 
        active_time=row['활동시간'],
        subject=row['종목'],
        other_objects=row['기타종목'],
        disability_type=row['장애유형'],
        permission_date=row['승인일']
    )
    new_clubs.append(club)

# 세션에 클럽 데이터 추가
session.add_all(new_clubs)

# 커밋하여 데이터베이스에 저장
session.commit()

# 세션 종료
session.close()