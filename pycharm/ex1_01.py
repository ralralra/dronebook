# 예제 1-1. 연결하고 상태 확인하기
# 1-1 드론 연결과 신호 출력

from drone_sim import *

drone = Drone()
drone.pair()

print("배터리:", drone.get_battery(), "%")
print("비행 상태:", drone.get_flight_state().name)
print("높이:", drone.get_height(), "cm")

drone.close()


# ----- 실행 결과 (가상 드론) -----
# [가상] 드론에 연결되었습니다. 배터리 100 %
# 배터리: 100 %
# 비행 상태: Ready
# 높이: 0.0 cm
# [가상] 연결을 닫았습니다.
