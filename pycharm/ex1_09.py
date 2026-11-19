# 예제 1-9. 방향에 따라 달라지는 이동
# 1-3 이동·회전 및 경로 제어

from drone_sim import *

drone = Drone()
drone.pair()
drone.takeoff()

drone.move_forward(100)
print(f"  방향 {drone.get_angle_z()}도에서 전진 → x={drone.get_pos_x():.0f}, y={drone.get_pos_y():.0f}")

drone.turn_left(90)
drone.move_forward(80)
print(f"  방향 {drone.get_angle_z()}도에서 전진 → x={drone.get_pos_x():.0f}, y={drone.get_pos_y():.0f}")

drone.land()
drone.close()


# ----- 실행 결과 (가상 드론) -----
# [가상] 드론에 연결되었습니다. 배터리 100 %
# [가상] 이륙. 고도 약 80 cm
# [가상] 앞으로 100cm
#   방향 0.0도에서 전진 → x=100, y=0
# [가상] 왼쪽으로 90도 회전
# [가상] 앞으로 80cm
#   방향 90.0도에서 전진 → x=100, y=80
# [가상] 착륙
# [가상] 연결을 닫았습니다.
