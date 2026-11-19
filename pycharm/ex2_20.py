# 예제 2-20. 바람에 따른 비행 경로 그리기
# 2-5 비행 기록 관리 및 분석
# 필요한 라이브러리: pandas, matplotlib
# 먼저 ex2_18.py 를 실행해야 합니다. 그 예제가 만든 파일을 이 예제가 읽습니다.

import pandas as pd
import matplotlib.pyplot as plt
import font_setup

fig, ax = plt.subplots(figsize=(5, 4))
for 바람, 모양 in zip([0, 2, 4], ["o-", "s--", "^:"]):
    df = pd.read_csv(f"flight_wind{바람}.csv")
    ax.plot(df["y"], df["x"], 모양, label=f"풍속 {바람} m/s")
ax.plot(0, 0, "k*", markersize=12, label="출발점")
ax.set_title("바람에 따른 사각형 비행 경로")
ax.set_xlabel("y (cm, 왼쪽 +)")
ax.set_ylabel("x (cm, 앞 +)")
ax.invert_xaxis()                     # 왼쪽(+y)이 그림의 왼쪽에 오도록
ax.set_aspect("equal")
ax.grid(True, linewidth=0.5)
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig("path_by_wind.png", dpi=150)
print("path_by_wind.png 저장")


# ----- 실행 결과 (가상 드론) -----
# path_by_wind.png 저장
