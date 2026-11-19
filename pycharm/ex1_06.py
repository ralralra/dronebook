# 예제 1-6. 이륙 → 정지 비행 → 착륙
# 1-2 상태 점검과 기본 비행 및 비상 대응

from drone_sim import *

drone = Drone()
drone.pair()
drone.takeoff()

print("[정지 비행 2초 동안 0.5초마다 높이 재기]")
for i in range(4):
    drone.hover(0.5)
    print(f"  {(i + 1) * 0.5:.1f}초  높이 {drone.get_height()} cm")

drone.land()
drone.close()


# ----- 실행 결과 (가상 드론) -----
# [가상] 드론에 연결되었습니다. 배터리 100 %
# [가상] 이륙. 고도 약 80 cm
# [정지 비행 2초 동안 0.5초마다 높이 재기]
#   0.5초  높이 79.48 cm
#   1.0초  높이 80.87 cm
#   1.5초  높이 80.0 cm
#   2.0초  높이 79.47 cm
# [가상] 착륙
# [가상] 연결을 닫았습니다.
