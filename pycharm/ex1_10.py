# 예제 1-10. 단위를 잘못 넣으면
# 1-3 이동·회전 및 경로 제어

from drone_sim import *

drone = Drone(verbose=False)
drone.pair()
drone.takeoff()

for 거리, 단위 in [(50, "cm"), (0.5, "m"), (50, "mm")]:
    전 = drone.get_pos_x()
    drone.move_forward(거리, 단위)
    후 = drone.get_pos_x()
    print(f"move_forward({거리}, '{단위}') → x가 {후 - 전:.0f} cm 바뀜")

drone.land()
drone.close()


# ----- 실행 결과 (가상 드론) -----
# move_forward(50, 'cm') → x가 50 cm 바뀜
# move_forward(0.5, 'm') → x가 50 cm 바뀜
# Error: Not a valid unit.
# move_forward(50, 'mm') → x가 0 cm 바뀜
