# 예제 3-8. 이동평균으로 다듬기
# 3-3 센서 데이터 처리와 동작 제어

from drone_sim import *
from collections import deque
import statistics

drone = Drone(verbose=False)
drone.pair()
drone.takeoff()
drone.sim_set_obstacle(100)

최근값 = deque(maxlen=4)                       # 최근 4개만 담는 상자
print(f"{'회':>2} {'측정값':>8} {'이동평균':>8}")
for i in range(8):
    값 = drone.get_front_range()
    최근값.append(값)
    print(f"{i + 1:>2} {값:>10.2f} {statistics.mean(최근값):>10.2f}")
drone.land()


# ----- 실행 결과 (가상 드론) -----
#  회      측정값     이동평균
#  1      98.61      98.61
#  2      98.58      98.59
#  3      99.89      99.03
#  4      99.46      99.13
#  5      99.64      99.39
#  6     101.18     100.04
#  7     100.08     100.09
#  8     100.18     100.27
