from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Users, Clubs, Club_members, Facilities, Subjects, Levels, DisabilityTypes
from datetime import datetime

# 세션을 생성합니다
session = SessionLocal()

# 데이터 삽입 예시

# 1. Users 테이블에 데이터 삽입
new_user = Users()
session.add(new_user)

# 2. Clubs 테이블에 데이터 삽입
new_club = Clubs(
    creator_id=new_user.id,
    facility_id=1,
    min_capacity=10,
    max_capacity=20,
    time=datetime.now(),
    repeat='weekly',
    start_period=datetime.now(),
    end_period=datetime.now(),
    fee=100,
    img_url="http://example.com/image.png",
    title="Tennis Club",
    content="Join us for a tennis session!"
)
session.add(new_club)

# 3. Club_members 테이블에 데이터 삽입
new_member = Club_members(
    club_id=new_club.id,
    user_id=new_user.id
)
session.add(new_member)

# 4. Facilities 테이블에 데이터 삽입
new_facility = Facilities(
    x=127,
    y=36,
    phone="010-1234-5678",
    road_address="Seoul, Gangnam-gu",
    img_url="http://example.com/facility_image.png",
    subject_ids="1",
    level_ids="1",
    disability_type_ids="1"
)
session.add(new_facility)

# 5. Subjects 테이블에 데이터 삽입
new_subject = Subjects(name="Tennis")
session.add(new_subject)

# 6. Levels 테이블에 데이터 삽입
new_level = Levels(name="Beginner", description="For beginners")
session.add(new_level)

# 7. DisabilityTypes 테이블에 데이터 삽입
new_disability_type = DisabilityTypes(name="None")
session.add(new_disability_type)

# 커밋하여 데이터베이스에 저장
session.commit()

# 세션 종료
session.close()