# 예제 3-4. 바람에 따른 기울기로 안정성 판단하기
# 3-2 자세·기압·색상 센서 활용

from drone_sim import *

위험각도 = 8

for 바람 in [0, 3, 6]:
    drone = Drone(verbose=False)
    drone.sim_set_wind(바람)                  # 가상 드론 전용
    drone.pair()
    drone.takeoff()
    측정 = [(drone.get_angle_x(), drone.get_angle_y()) for _ in range(10)]
    최대 = max(max(abs(a), abs(b)) for a, b in 측정)
    판정 = "위험 - 착륙" if 최대 >= 위험각도 else ("주의" if 최대 >= 위험각도 / 2 else "안정")
    print(f"풍속 {바람} m/s - 10번 잰 기울기 중 최대 {최대:4.1f}도 → {판정}")
    drone.land()


# ----- 실행 결과 (가상 드론) -----
# 풍속 0 m/s - 10번 잰 기울기 중 최대  1.0도 → 안정
# 풍속 3 m/s - 10번 잰 기울기 중 최대  3.4도 → 안정
# 풍속 6 m/s - 10번 잰 기울기 중 최대  5.8도 → 주의
