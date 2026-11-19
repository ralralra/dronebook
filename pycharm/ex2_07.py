# 예제 2-7. 목표 쪽으로 돌아서 가기
# 2-2 표준 라이브러리 활용

from drone_sim import *
import math

drone = Drone(verbose=False)
drone.pair()
drone.takeoff()

for 목표 in [(100, 100), (0, 100)]:
    dx = 목표[0] - drone.get_pos_x()
    dy = 목표[1] - drone.get_pos_y()
    필요한방향 = math.degrees(math.atan2(dy, dx))
    돌각도 = 필요한방향 - drone.get_angle_z()
    if 돌각도 >= 0:
        drone.turn_left(round(돌각도))
    else:
        drone.turn_right(round(-돌각도))
    drone.move_forward(round(math.hypot(dx, dy)))
    print(f"목표 {목표} → 현재 ({round(drone.get_pos_x())}, {round(drone.get_pos_y())}), 방향 {drone.get_angle_z()}도")

drone.land()
drone.close()


# ----- 실행 결과 (가상 드론) -----
# 목표 (100, 100) → 현재 (100, 100), 방향 45.0도
# 목표 (0, 100) → 현재 (0, 100), 방향 -180.0도
