import pandas as pd

# 데이터 파일 로드
df = pd.read_excel('data/club_data.xlsx')

# 컬럼명 출력
print("데이터프레임의 컬럼명:")
print(df.columns)
