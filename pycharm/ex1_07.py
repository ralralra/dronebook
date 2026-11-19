# 예제 1-7. 상황에 따라 다르게 대응하기
# 1-2 상태 점검과 기본 비행 및 비상 대응

from drone_sim import *

drone = Drone()
drone.pair()
drone.takeoff()

상황 = "배터리부족"        # "사람접근", "기울어짐" 등으로 바꾸어 보세요

if 상황 == "사람접근":
    print("!! 사람 접근 - 비상 정지")
    drone.emergency_stop()
elif 상황 == "기울어짐":
    print("!! 자세 불안정 - 비상 정지")
    drone.emergency_stop()
elif 상황 == "배터리부족":
    print("!! 배터리 부족 - 착륙")
    drone.land()
else:
    print("알 수 없는 상황 - 착륙")
    drone.land()

print("지금 비행 상태:", drone.get_flight_state().name)
drone.close()


# ----- 실행 결과 (가상 드론) -----
# [가상] 드론에 연결되었습니다. 배터리 100 %
# [가상] 이륙. 고도 약 80 cm
# !! 배터리 부족 - 착륙
# [가상] 착륙
# 지금 비행 상태: Ready
# [가상] 연결을 닫았습니다.
