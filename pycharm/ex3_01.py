# 예제 3-1. 앞 거리와 고도 읽기
# 3-1 거리·고도 센서 활용

from drone_sim import *

drone = Drone(verbose=False)
drone.pair()
drone.takeoff()
drone.sim_set_obstacle(120)           # 가상 드론 전용: 앞 120 cm 에 벽

print("같은 자리에서 다섯 번 재기")
for i in range(5):
    print(f"  {i + 1}회  앞 {drone.get_front_range():7.2f} cm   고도 {drone.get_height():6.2f} cm")

drone.sim_set_obstacle(None)          # 벽을 치운다
print("벽이 없을 때 앞 센서:", drone.get_front_range())
drone.land()


# ----- 실행 결과 (가상 드론) -----
# 같은 자리에서 다섯 번 재기
#   1회  앞  118.61 cm   고도  78.58 cm
#   2회  앞  119.89 cm   고도  79.46 cm
#   3회  앞  119.64 cm   고도  81.18 cm
#   4회  앞  120.08 cm   고도  80.18 cm
#   5회  앞  119.21 cm   고도  78.57 cm
# 벽이 없을 때 앞 센서: 999
