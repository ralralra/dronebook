# 예제 3-14. 제어 결과를 그래프로 비교하기
# 3-4 피드백과 비례 제어
# 필요한 라이브러리: matplotlib

from drone_sim import *
import matplotlib.pyplot as plt
import font_setup

def 제어실험(Kp, 목표=120, 횟수=60):
    drone = Drone(verbose=False)
    drone.pair()
    drone.takeoff()
    기록 = []
    for i in range(횟수):
        오차 = 목표 - drone.get_height()
        drone.set_throttle(max(-100, min(100, round(Kp * 오차))))
        drone.move(0.1)
        기록.append(drone.get_height())
    drone.land()
    return 기록

시간 = [(i + 1) * 0.1 for i in range(60)]
fig, ax = plt.subplots(figsize=(5.6, 3.4))
for Kp, 모양 in zip([0.5, 1.0, 3.0, 6.0], ["-", "--", "-.", ":"]):
    ax.plot(시간, 제어실험(Kp), 모양, label=f"Kp = {Kp}")
ax.axhline(120, color="gray", linewidth=1)
ax.text(0.2, 122, "목표 120 cm", fontsize=9, color="gray")
ax.set_title("비례 상수에 따른 고도 변화")
ax.set_xlabel("시간 (초)")
ax.set_ylabel("고도 (cm)")
ax.legend(fontsize=8)
ax.grid(True, linewidth=0.5)
fig.tight_layout()
fig.savefig("control.png", dpi=150)
print("control.png 저장")


# ----- 실행 결과 (가상 드론) -----
# control.png 저장
