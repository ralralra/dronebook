# 예제 3-15. 라이브러리의 거리 유지 기능
# 3-4 피드백과 비례 제어

from drone_sim import *

drone = Drone(verbose=False)
drone.pair()
drone.takeoff()
drone.sim_set_obstacle(130)                   # 가상 드론 전용: 앞 130 cm 에 벽

print("시작 - 앞 거리", drone.get_front_range(), "cm")
drone.keep_distance(timeout=3, distance=50)    # 3초 동안 50 cm 유지
print("3초 뒤 - 앞 거리", drone.get_front_range(), "cm")
drone.land()


# ----- 실행 결과 (가상 드론) -----
# 시작 - 앞 거리 128.61 cm
# 3초 뒤 - 앞 거리 55.19 cm
