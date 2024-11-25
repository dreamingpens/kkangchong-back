from fastapi import FastAPI
from pydantic import BaseModel
import openai
import re
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()  # .env 파일에서 환경변수 로드
openai.api_key = os.getenv('OPENAI_API_KEY')
# anthropic = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

# 사용자 입력 데이터 모델
class UserInput(BaseModel):
    arm_angle: float  # 팔을 양옆으로 들 수 있는 각도 (0-180도)
    torso_left_angle: float  # 허리를 왼쪽으로 돌릴 수 있는 각도 (0-70도)
    torso_right_angle: float  # 허리를 오른쪽으로 돌릴 수 있는 각도 (0-70도)
    body_left_tilt: float  # 몸을 왼쪽으로 기울일 수 있는 각도 (0-80도)
    body_right_tilt: float  # 몸을 오른쪽으로 기울일 수 있는 각도 (0-80도)
    core_strength_time: float  # 등받이에 등을 떼고 허리를 세울 수 있는 시간 (초)
    punch_count: int  # 10초 안에 허공에 주먹 지르기 횟수

# 추천 결과 데이터 모델
class RecommendationOutput(BaseModel):
    basketball_score: int
    basketball_reason: str
    table_tennis_score: int
    table_tennis_reason: str
    rugby_score: int
    rugby_reason: str
    fencing_score: int
    fencing_reason: str
    dance_sports_score: int
    dance_sports_reason: str
    athletics_score: int
    athletics_reason: str

# FastAPI 애플리케이션 초기화
app = FastAPI()

# CORS 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# LLM 호출 함수
def call_llm(prompt: str) -> str:
    """
    OpenAI API를 사용하여 프롬프트를 전달하고 응답을 반환합니다.
    """
    system_prompt = """
    당신은 장애인 스포츠 추천 전문가입니다. 
    사용자의 신체 능력을 바탕으로 각 스포츠에 대한 추천 점수(0-5점)와 이유를 제공해주세요.
    
    다음과 같은 형식으로 응답해주세요:
    농구 점수: [점수]점
    이유: [이유]
    
    탁구 점수: [점수]점
    이유: [이유]
    
    럭비 점수: [점수]점
    이유: [이유]
    
    펜싱 점수: [점수]점
    이유: [이유]
    
    댄스스포츠 점수: [점수]점
    이유: [이유]
    
    육상 점수: [점수]점
    이유: [이유]
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

# 프롬프트 생성 함수
def generate_prompt(user_input: UserInput) -> str:
    """
    사용자 데이터를 기반으로 LLM에 전달할 프롬프트를 생성합니다.
    """
    criteria_and_example = """
    추천 점수 체계:
	  0 이상 5 이하의 정수
	  예시
		1. 운동 능력이 전혀 부족함 (추천 점수: 0)
		2. 약간의 운동이 가능하나 큰 제한이 있음 (추천 점수: 1)
		3. 평균 이하의 운동 능력 (추천 점수: 2)
		4. 평균 수준의 운동 능력 (추천 점수: 3)
		5. 대부분의 동작이 가능함 (추천 점수: 4)
		6. 모든 동작이 가능하고, 안정적임 (추천 점수: 5)

    사용자 데이터:
    - 팔을 양옆으로 들 수 있는 각도 - 최대 180도
    - 허리를 왼쪽으로 돌릴 수 있는 각도 - 70도 이상인 경우 충분
    - 허리를 오른쪽으로 돌릴 수 있는 각도 - 70도 이상인 경우 충분
    - 몸을 왼쪽으로 기울일 수 있는 각도 - 80도 이상이면 충분
    - 몸을 오른쪽으로 기울일 수 있는 각도 - 80도 이상이면 충분
    - 코어 힘 (등받이에 등을 떼고 허리를 세울 수 있는 시간) - 60초 이상이면 충분
    - 팔 근력 (10초 안에 허공에 주먹 지르기 횟수) - 30회 이상이면 충분, 0회면 운동 불가
    
    운동 추천 기준:
    1. 휠체어 농구:
       # 등급별 참여 가능 기준
       - 1.0등급(운동 어려움): 
         * 수직/회전면 운동 시 능동적 몸통 움직임이 어려운 선수
         * 전/후면 운동 시 제한된 조절만 가능
         * 교정이 필요할 때는 외부 지지 필요
       
       - 2.0등급(부분적으로 운동 가능):
         * 능동적 상부 몸통 회전 가능
         * 전면 운동 시 부분적 조절 가능
         * 측면 운동 조절은 제한적
       
       - 3.0~4.5등급(운동 가능):
         * 수직/회전/전후면 운동 시 완전한 조절 가능
         * 상황에 따른 적절한 몸통 움직임 구사 가능
         * 더 높은 등급일수록 더 자유로운 움직임 가능

    2. 휠체어 탁구:
       # TT등급별 참여 가능 기준
       - TT1-2등급(운동 가능):
         * 시상면과 전두면에서 몸통의 자유로운 운동이 가능함
         * 그립, 완관절, 주관절 기능이 자유로움
       
       - TT2-3등급(부분적으로 운동 가능):
         * 그립(쥐기)과 완관절의 굴곡/신전 기능이 제한적인 선수
         * 상두박근 기능이 매우 제한적이거나 없는 경우
       
       - TT3-4등급(운동 어려움):
         * 등받이가 없으면 휠체어에 앉을 때 균형이 좋지 않음
         * 상부 몸통을 조정하고 요추부를 고정하는 복근과 배근이 없음
       
       - TT4-5등급(운동 불가):
         * 고관절과 허벅지 근육이 없기 때문에 바른 자세 유지 어려움
         * 상부 몸통 조절 불가
         * 시상면과 전두면에서 몸통 움직임 제한

    3. 휠체어 럭비:
       # 등급별 참여 가능 기준
       - 1등급 선수(운동 불가):
         * 모든 면에서 몸통 운동이 어렵거나 제한적
         * 앞, 뒷면에서의 균형이 현저히 떨어짐
         * 외부 지지 필요시 균형 보조 필요
         * 능동적 몸통 움직임이 제한적
       
       - 2등급 선수(운동 어려움):
         * 앞, 뒷면에서의 능동적 운동 일부 가능
         * 좌우 움직임은 제한적
         * 몸통 상부의 회전은 하부 회전보다 원활
       
       - 3등급 선수 (부분적으로 운동 가능):
         * 앞, 뒷면에서의 몸통 운동이 자유로움
         * 몸통 회전이 자유롭지만 좌우 움직임은 제한적
       
       - 4~4.5등급 선수 (운동 가능):
         * 몸통 운동이 전반적으로 자유로움
         * 모든 방향에서의 움직임이 가능
         * 한쪽으로의 움직임에도 제한이 거의 없음

    4. 휠체어 펜싱:
       # 등급별 참여 가능 기준
       - 1A등급(운동 불가):
         * 좌식 균형이 전혀 없는 선수
         * 팔꿈치 신전이 효과적으로 이루어지지 않음
         * 손 기능이 매우 제한적이어서 펜싱 칼을 붕대로 고정 필요
         * 주로 C5/C6 척수 손상 수준의 사지마비 선수
       
       - 1B등급(운동 어려움):
         * 앉은 자세 균형 없음
         * 팔꿈치 신전은 가능하나 손가락 굴곡 기능 없음
         * 펜싱 칼은 여전히 붕대로 고정 필요
         * 주로 C7/C8 수준의 사지마비 선수
       
       - 2등급(부분적으로 운동 가능):
         * 적절한 좌식 균형 보유
         * 펜싱 팔 기능이 정상에 가까움
         * 손가락과 손목의 근력이 중간 이상
         * 주로 T1-T9 수준의 하반신 마비 선수
       
       - 3등급(운동 가능):
         * 좋은 좌식 균형
         * 정상적인 펜싱 팔 기능
         * 하지 지지는 제한적
         * 주로 T10-L2 수준의 하반신 마비 선수

    5. 댄스스포츠:
       # 기능 수준별 참여 가능 기준
       - 중증 제한 수준:
         * 골반 움직임: 
           - 자발적인 골반 움직임 불가
           - 외부 지지 없이는 앉은 자세 유지 어려움
         * 몸통 힘:
           - 앞/옆 방향으로 몸통을 숙일 때 즉각적인 자세 회복 불가
           - 무게중심 이동 시 균형 상실
         * 몸통 회전:
           - 회전 동작 시도 자체가 어려움
           - 회전 시 심각한 균형 상실
         * 머리/목 조절:
           - 머리 위치 유지가 어려움
           - 목의 자발적 움직임 매우 제한적
       
       - 중등도 제한 수준:
         * 골반 움직임:
           - 제한된 범위 내에서 골반 움직임 가능
           - 한쪽 방향으로만 움직임 조절 가능
         * 몸통 힘:
           - 부분적으로 앞으로 구부리기 가능
           - 제한된 범위의 옆으로 기울이기 가능
         * 몸통 회전:
           - 부분적인 회전 가능하나 불안정
           - 천천히 움직일 때만 균형 유지 가능
         * 머리/목 조절:
           - 제한된 범위의 머리 움직임
           - 동적 움직임 중 간헐적 조절 가능
       - 경도 제한 수준:
         * 골반 움직임:
           - 대부분의 방향으로 골반 움직임 가능
           - 동적 움직임 중에도 어느 정도 안정성 유지
         * 몸통 힘:
           - 대부분의 앞/옆 구부리기 동작 가능
           - 자세 회복이 비교적 원활
         * 몸통 회전:
           - 대부분의 회전 동작 수행 가능
           - 중간 속도의 움직임에서 균형 유지
         * 머리/목 조절:
           - 대부분의 머리/목 움직임 가능
           - 동적 움직임 중에도 안정적 조절
       
       - 최소 제한 수준:
         * 골반 움직임:
           - 모든 방향으로의 자유로운 골반 움직임
           - 높은 수준의 동적 안정성
         * 몸통 힘:
           - 완전한 범위의 앞/옆 구부리기 가능
           - 신속한 자세 회복
         * 몸통 회전:
           - 완전한 회전 동작 가능
           - 빠른 속도에서도 균형 유지
         * 머리/목 조절:
           - 자유로운 머리/목 움직임
           - 모든 동작에서 안정적 조절

    6. 휠체어 육상:
       # T등급별 참여 가능 기준
       
       - T51등급:
         * 상지 기능:
           - 어깨 움직임이 매우 제한적
           - 팔꿈치 굽히기/펴기 어려움
           - 손목과 손가락 움직임 심각하게 제한
         * 손 기능:
           - 내부 근육 기능 거의 없음
           - 물건 쥐기/잡기 동작 어려움
         * 몸통 기능:
           - 몸통 조절 능력 없음
           - 균형 유지 매우 어려움
       
       - T52등급:
         * 상지 기능:
           - T51보다 약간 나은 어깨 움직임
           - 제한적이지만 팔꿈치 조절 가능
           - 부분적인 손목 움직임 가능
         * 손 기능:
           - 매우 기본적인 쥐기 가능
           - 제한된 손가락 조절
         * 몸통 기능:
           - 제한적인 몸통 안정성
           - 기본적인 균형 유지 가능
       
       - T53등급:
         * 상지 기능:
           - 정상에 가까운 어깨 기능
           - 좋은 팔꿈치 조절
           - 손목과 손가락 기능 양호
         * 몸통 기능:
           - 복부 근육 기능 없거나 매우 낮음
           - 낮은 척추 기능
         * 휠체어 조작:
           - 능숙한 상지 사용으로 휠체어 조작 가능
           - 방향 전환과 가속 능력 양호
       
       - T54등급:
         * 상지 기능:
           - 완전한 상지 기능
           - 정교한 손동작 가능
         * 몸통 기능:
           - 부분적이거나 정상적인 몸통 기능
           - 복부 근육 사용 가능
         * 휠체어 조작:
           - 매우 숙련된 휠체어 조작
           - 빠른 가속과 정교한 방향 전환 가능
           - 몸통 회전을 활용한 추진력 생성 가능

       # 주요 경기력 영향 요소
       - 추진력 생성:
         * T51-52: 제한된 상지 기능으로 인한 약한 추진력
         * T53: 좋은 상지 기능으로 안정적 추진력
         * T54: 몸통 회전을 활용한 강력한 추진력
       
       - 코너링 능력:
         * T51-52: 제한된 방향 전환
         * T53: 안정적인 코너링
         * T54: 고속에서도 안정적인 코너링

    ---

    예시:
    사용자 데이터:
    - 팔을 양옆으로 들 수 있는 각도: 70도
    - 허리를 왼쪽으로 돌릴 수 있는 각도: 30도
    - 허리를 오른쪽으로 돌릴 수 있는 각도: 30도
    - 몸을 왼쪽으로 기울일 수 있는 각도: 25도
    - 몸을 오른쪽으로 기울일 수 있는 각도: 25도
    - 코어 힘 (허리를 세울 수 있는 시간): 50초
    - 팔 근력 (팔을 뻗고 유지 가능한 시간): 40초

    결과:
    - 농구 점수: 4점
      이유: 사용자의 팔을 양옆으로 드는 능력이 약간 제한적이지만, 팔 근력이 양호하고 코어 힘이 안정적입니다. 허리 회전이 균형적이나 각도가 조금 낮아 몸통의 회전 속도에 약간의 제한이 있을 수 있습니다.
    - 탁구 점수: 3점
      이유: 몸통 회전 각도와 기울임이 적절하나, 빠른 회전 동작에서 다소 부족할 수 있습니다. 코어 힘이 비교적 안정적이어서 기본적인 탁구 동작 수행에는 문제가 없습니다.
    - 럭비 점수: 2점
      이유: 강한 몸통 조절과 다방향 움직임이 필요한 럭비에 비해 허리 회전 각도가 낮고 코어 힘이 다소 부족합니다. 상체의 안정성은 어느 정도 유지되지만, 격한 움직임에서 어려움이 예상됩니다.
    - 펜싱 점수: 3점
      이유: 팔 근력은 적절하고 허리 회전도 가능하지만, 앉은 자세에서의 빠른 균형 조절 능력이 약간 부족할 수 있습니다. 방향 전환 시 안정성을 유지하는 데 약간의 제한이 있을 것입니다.
    - 댄스스포츠 점수: 4점
      이유: 골반과 몸통의 움직임이 적절하며, 기본적인 코어 힘이 안정적입니다. 빠른 회전 동작에서 약간의 제한이 있을 수 있지만, 대부분의 동작을 수행하는 데 무리가 없습니다.
    - 육상 점수: 4점
      이유: 상지 기능과 코어 힘이 적절하여 휠체어 조작에 유리합니다. 직선 주행에서 안정성이 있으며, 몸통의 회전이 자유롭지는 않지만 기본적인 추진력 생성에 무리가 없습니다.
    
    ---
    """

    user_data = f"""
    실제 입력:
    사용자 데이터:
    - 팔을 양옆으로 들 수 있는 각도: {user_input.arm_angle}도
    - 허리를 왼쪽으로 돌릴 수 있는 각도: {user_input.torso_left_angle}도
    - 허리를 오른쪽으로 돌릴 수 있는 각도: {user_input.torso_right_angle}도
    - 몸을 왼쪽으로 기울일 수 있는 각도: {user_input.body_left_tilt}도
    - 몸을 오른쪽으로 기울일 수 있는 각도: {user_input.body_right_tilt}도
    - 코어 힘 (등받이에 등을 떼고 허리를 세울 수 있는 시간): {user_input.core_strength_time}초
    - 팔 근력 (10초 안에 허공에 주먹 지르기 횟수): {user_input.punch_count}회

    결과:
    """
    return criteria_and_example + user_data

# LLM 응답 파싱 함수
def parse_llm_output(llm_output: str) -> dict:
    """
    LLM에서 받은 응답 텍스트를 파싱하여 각 운동의 추천 점수와 이유를 추출합니다.
    """
    results = {
        "basketball_score": 0,
        "basketball_reason": "",
        "table_tennis_score": 0,
        "table_tennis_reason": "",
        "rugby_score": 0,
        "rugby_reason": "",
        "fencing_score": 0,
        "fencing_reason": "",
        "dance_sports_score": 0,
        "dance_sports_reason": "",
        "athletics_score": 0,
        "athletics_reason": ""
    }

    # 정규표현식 패턴 수정
    patterns = {
        "basketball": r"농구\s*점수:\s*(\d+)점\s*이유:\s*([^\n]+)",
        "table_tennis": r"탁구\s*점수:\s*(\d+)점\s*이유:\s*([^\n]+)",
        "rugby": r"럭비\s*점수:\s*(\d+)점\s*이유:\s*([^\n]+)",
        "fencing": r"펜싱\s*점수:\s*(\d+)점\s*이유:\s*([^\n]+)",
        "dance_sports": r"댄스스포츠\s*점수:\s*(\d+)점\s*이유:\s*([^\n]+)",
        "athletics": r"육상\s*점수:\s*(\d+)점\s*이유:\s*([^\n]+)"
    }

    for sport, pattern in patterns.items():
        match = re.search(pattern, llm_output, re.MULTILINE | re.DOTALL)
        if match:
            results[f"{sport}_score"] = int(match.group(1))
            results[f"{sport}_reason"] = match.group(2).strip()

    # 디버깅을 위한 로그 출력
    print("LLM Response:", llm_output)
    print("Parsed Results:", results)

    return results

# API 엔드포인트 정의
@app.post("/recommend", response_model=RecommendationOutput)
async def recommend_activity(user_input: UserInput):
    """
    사용자 입력 데이터를 받아 LLM을 통해 운동 추천 결과를 반환합니다.
    """
    # 프롬프트 생성
    prompt = generate_prompt(user_input)
    
    # LLM 호출
    llm_response = call_llm(prompt)
    
    # LLM 응답 파싱
    results = parse_llm_output(llm_response)
    
    return RecommendationOutput(**results)
