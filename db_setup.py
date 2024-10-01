from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Users, Clubs, Club_members, Facilities, Subjects, Levels, RecommendedTargets
from datetime import datetime, date
# 세션을 생성합니다
session = SessionLocal()

# 데이터 삽입 예시

# 1. Users 테이블에 데이터 삽입
new_user = Users(id=1, name="장원준")
session.add(new_user)

# 2. Clubs 테이블에 데이터 삽입
new_club = Clubs(
    id = 1,
    creator_id=new_user.id,
    facility_id=1,
    min_capacity=10,
    max_capacity=20,
    time=datetime.now(),
    start_period=date.today(),
    end_period=date.today(),
    fee=1000,
    img_url="https://loremflickr.com/320/240/tennis",
    title="Tennis Club",
    content="테니스 클럽에 아무나 들어오세요!"
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
    id=1,
    phone="02-871-3636",
    road_address="서울 관악구 보라매로 44 2층",
    img_urls="https://img1.kakaocdn.net/cthumb/local/R0x420.q50/?fname=https%3A%2F%2Fpostfiles.pstatic.net%2FMjAyMzAzMDhfMjc2%2FMDAxNjc4MjQ5OTAyNjA0.6MUglHvKW3QZCeki_vsPEYHIgp8dZOdhXCsnDf2HGBIg.miLVtlUmsgt7DANuwyysqqI1nn-eaaDBcCVdr9cHS0cg.JPEG.b1a49923%2FIMG_1379.jpg%3Ftype%3Dw773",
    subject_ids=1,
    level_ids=1,
    disability_type_ids=1
)
session.add(new_facility)

# 5. Subjects 테이블에 데이터 삽입
new_subjects = [
    Subjects(name="수상스포츠"),
    Subjects(name="구기운동"),
    Subjects(name="싸이클"),
    Subjects(name='육상'),
    Subjects(name='라켓 스포츠'),
    Subjects(name="기타")
]
session.add_all(new_subjects)

# 6. Levels 테이블에 데이터 삽입
new_levels = [
    Levels(name="초급", description="운동을 거의 해본적이 없는 사람"),
    Levels(name="중급", description="기초적인 운동 방법을 숙지하고 있고 3개월 이상의 경력이 있는 사람"),
    Levels(name="상급", description="1년 이상의 해당 운동을 한 경력이 있으며 심화 내용 또한 숙지하고 있음"),
    Levels(name="마스터", description="대회 준비 / 선수 준비를 위해 전문적으로 운동을 하는 사람")
]
session.add_all(new_levels)

# 7. DisabilityTypes 테이블에 데이터 삽입
new_disability_types = [
    RecommendedTargets(name="20대 이하"),
    RecommendedTargets(name="30대"),
    RecommendedTargets(name="40대"),
    RecommendedTargets(name="50대 이상"),
]
session.add_all(new_disability_types)

# 커밋하여 데이터베이스에 저장
session.commit()

# 세션 종료
session.close()