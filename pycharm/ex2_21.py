# 예제 2-21. 비행 성적표 만들기
# 2-5 비행 기록 관리 및 분석
# 필요한 라이브러리: pandas
# 먼저 ex2_18.py 를 실행해야 합니다. 그 예제가 만든 파일을 이 예제가 읽습니다.

import pandas as pd
import math

결과 = []
for 바람 in [0, 2, 4]:
    df = pd.read_csv(f"flight_wind{바람}.csv")
    끝 = df.iloc[-1]
    결과.append({
        "바람": 바람,
        "경로오차": round(math.dist((0, 0), (끝["x"], 끝["y"])), 1),
        "사용배터리": df["배터리"].iloc[0] - 끝["배터리"],
    })

성적표 = pd.DataFrame(결과)
성적표["효율"] = (800 / 성적표["사용배터리"]).round(1)      # 1 % 로 날 수 있는 거리(cm)
print(성적표.to_string(index=False))


# ----- 실행 결과 (가상 드론) -----
#  바람  경로오차  사용배터리    효율
#   0   0.0      6 133.3
#   2  82.1      7 114.3
#   4 164.2      7 114.3
