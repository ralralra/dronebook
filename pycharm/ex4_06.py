# 예제 4-6. 연습용 비행 판단 데이터 만들기
# 4-2 규칙 기반 제어와 기계학습의 비교
# 필요한 라이브러리: pandas

import numpy as np
import pandas as pd

난수 = np.random.default_rng(20)
개수 = 400

# (1) 실제 상황 - 우리는 직접 알 수 없다
실제거리 = 난수.uniform(20, 150, 개수)
실제기울기 = 난수.uniform(0, 14, 개수)
배터리 = 난수.integers(10, 100, 개수)

# (2) 정답은 실제 상황으로 정한다
정답 = ((실제거리 >= 50) & (실제기울기 <= 8) & (배터리 >= 30)).astype(int)

# (3) 기록에 남는 것은 잡음이 섞인 센서 값이다
df = pd.DataFrame({
    "거리": np.round(실제거리 + 난수.normal(0, 4, 개수), 1),
    "기울기": np.round(실제기울기 + 난수.normal(0, 0.8, 개수), 1),
    "배터리": 배터리,
    "계속": 정답,
})
df.to_csv("flight_decision.csv", index=False, encoding="utf-8-sig")
print(df.head())
print(f"전체 {len(df)}건 - 계속 {df['계속'].sum()}건, 중단 {len(df) - df['계속'].sum()}건")


# ----- 실행 결과 (가상 드론) -----
#      거리   기울기  배터리  계속
# 0  62.5  10.7   16   0
# 1  80.7   8.8   57   0
# 2  38.9   2.2   32   0
# 3  83.9   5.3   79   1
# 4  70.5  14.6   84   0
# 전체 400건 - 계속 140건, 중단 260건
