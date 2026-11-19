# 예제 3-9. 멈추는 기준과 가는 기준을 다르게
# 3-3 센서 데이터 처리와 동작 제어

from drone_sim import *

def 판단_기준하나(거리, 상태):
    return "정지" if 거리 < 60 else "전진"

def 판단_기준둘(거리, 상태):
    if 상태 == "전진" and 거리 < 60:        # 60 보다 가까워지면 멈추고
        return "정지"
    if 상태 == "정지" and 거리 > 70:        # 70 보다 멀어져야 다시 간다
        return "전진"
    return 상태

drone = Drone(verbose=False)
drone.pair()
drone.takeoff()
drone.sim_set_obstacle(60)
측정값 = [drone.get_front_range() for _ in range(12)]
drone.land()

for 이름, 판단함수 in [("기준 하나", 판단_기준하나), ("기준 둘", 판단_기준둘)]:
    상태, 기록 = "전진", []
    for 거리 in 측정값:
        상태 = 판단함수(거리, 상태)
        기록.append(상태[0])                 # '전' 또는 '정' 한 글자만
    바뀜 = sum(1 for a, b in zip(기록, 기록[1:]) if a != b)
    print(f"{이름}: {' '.join(기록)}  (바뀜 횟수 {바뀜})")


# ----- 실행 결과 (가상 드론) -----
# 기준 하나: 정 정 정 정 정 전 전 전 정 정 정 정  (바뀜 횟수 2)
# 기준 둘: 정 정 정 정 정 정 정 정 정 정 정 정  (바뀜 횟수 0)
