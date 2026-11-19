# 예제 1-11. 좌표로 경로 비행하기
# 1-3 이동·회전 및 경로 제어

from drone_sim import *

경유지 = [(100, 0), (100, 80), (0, 80), (0, 0)]     # (x, y) cm

drone = Drone(verbose=False)
drone.pair()
drone.takeoff()

for 목표x, 목표y in 경유지:
    dx = (목표x - drone.get_pos_x()) / 100            # cm → m
    dy = (목표y - drone.get_pos_y()) / 100
    drone.move_distance(dx, dy, 0, 0.5)
    print(f"목표 ({목표x}, {목표y}) → 현재 ({drone.get_pos_x():.0f}, {drone.get_pos_y():.0f})")

drone.land()
drone.close()


# ----- 실행 결과 (가상 드론) -----
# 목표 (100, 0) → 현재 (100, 0)
# 목표 (100, 80) → 현재 (100, 80)
# 목표 (0, 80) → 현재 (0, 80)
# 목표 (0, 0) → 현재 (0, 0)
