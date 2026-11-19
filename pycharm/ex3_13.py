# 예제 3-13. 비례 상수에 따른 결과 비교
# 3-4 피드백과 비례 제어

from drone_sim import *

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
    drone.reset_move_values()
    drone.land()
    return 기록

목표 = 120
print(f"{'Kp':>4} {'최고 고도':>8} {'목표 초과':>8} {'마지막 고도':>9} {'115 cm 도달':>10}")
for Kp in [0.5, 1.0, 3.0, 6.0]:
    기록 = 제어실험(Kp)
    초과 = max(0, max(기록) - 목표)
    도달 = next((i for i, h in enumerate(기록) if h >= 115), None)
    도달표시 = f"{(도달 + 1) * 0.1:.1f}초" if 도달 is not None else "못 미침"
    print(f"{Kp:>4} {max(기록):>10.1f} {초과:>10.1f} {기록[-1]:>11.1f} {도달표시:>10}")


# ----- 실행 결과 (가상 드론) -----
#   Kp    최고 고도    목표 초과    마지막 고도  115 cm 도달
#  0.5      119.7        0.0       117.8       3.5초
#  1.0      121.7        1.7       119.0       1.8초
#  3.0      129.7        9.7       118.5       0.6초
#  6.0      136.4       16.4       114.0       0.6초
