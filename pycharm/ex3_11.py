# 예제 3-11. 결과를 확인하지 않는 제어
# 3-4 피드백과 비례 제어

from drone_sim import *

목표고도 = 120
drone = Drone(verbose=False)
drone.pair()
drone.takeoff()

drone.set_throttle(30)               # 적당해 보이는 출력을 정해 두고
for i in range(30):                  # 3초 동안 그대로 민다
    drone.move(0.1)
drone.reset_move_values()

실제 = drone.get_height()
print(f"목표 {목표고도} cm, 실제 {실제} cm, 오차 {round(목표고도 - 실제, 1)} cm")
drone.land()


# ----- 실행 결과 (가상 드론) -----
# 목표 120 cm, 실제 999.9 cm, 오차 -879.9 cm
