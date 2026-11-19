# 예제 2-8. 평균과 중앙값 비교하기
# 2-2 표준 라이브러리 활용

from drone_sim import *
import statistics

drone = Drone(verbose=False)
drone.pair()
drone.takeoff()
drone.sim_set_obstacle(120)           # 가상 드론 전용: 앞 120 cm 에 벽

측정값 = [drone.get_front_range() for _ in range(6)]
drone.sim_set_obstacle(None)          # 벽을 치워 '튀는 값'을 하나 만든다
측정값.append(drone.get_front_range())
print("일곱 번 측정:", 측정값)
print("평균        :", round(statistics.mean(측정값), 1))
print("중앙값      :", statistics.median(측정값))
print("앞의 여섯 개 평균:", round(statistics.mean(측정값[:6]), 1))
drone.land()


# ----- 실행 결과 (가상 드론) -----
# 일곱 번 측정: [118.61, 118.58, 119.89, 119.46, 119.64, 121.18, 999]
# 평균        : 245.2
# 중앙값      : 119.64
# 앞의 여섯 개 평균: 119.6
