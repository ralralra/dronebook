# 예제 3-7. 잡음 때문에 판단이 흔들리는 모습
# 3-3 센서 데이터 처리와 동작 제어

from drone_sim import *

안전거리 = 60
drone = Drone(verbose=False)
drone.pair()
drone.takeoff()
drone.sim_set_obstacle(60)                    # 가상 드론 전용: 벽이 딱 경계에 있다

판단들 = []
for i in range(10):
    거리 = drone.get_front_range()
    판단 = "정지" if 거리 < 안전거리 else "전진"
    판단들.append(판단)
    print(f"  {i + 1:2d}회  {거리:6.2f} cm → {판단}")

바뀜 = sum(1 for a, b in zip(판단들, 판단들[1:]) if a != b)
print(f"판단이 바뀜 횟수: {바뀜}번")
drone.land()


# ----- 실행 결과 (가상 드론) -----
#    1회   58.61 cm → 정지
#    2회   58.58 cm → 정지
#    3회   59.89 cm → 정지
#    4회   59.46 cm → 정지
#    5회   59.64 cm → 정지
#    6회   61.18 cm → 전진
#    7회   60.08 cm → 전진
#    8회   60.18 cm → 전진
#    9회   59.21 cm → 정지
#   10회   58.57 cm → 정지
# 판단이 바뀜 횟수: 2번
