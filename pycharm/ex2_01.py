# 예제 2-1. 기본값을 가진 비행 함수
# 2-1 함수와 예외 처리

from drone_sim import *

def 다각형비행(drone, 변길이=100, 변수=4):
    """변의 수만큼 전진과 왼쪽 회전을 되풀이한다. 값을 생략하면 한 변 100 cm 사각형."""
    각도 = 360 // 변수
    for i in range(변수):
        drone.move_forward(변길이)
        drone.turn_left(각도)

drone = Drone(verbose=False)
drone.pair()
drone.takeoff()

다각형비행(drone)                      # 기본값 사용: 100 cm 사각형
print(f"사각형 뒤 위치: ({round(drone.get_pos_x())}, {round(drone.get_pos_y())}), 방향 {drone.get_angle_z()}도")
다각형비행(drone, 80, 3)               # 한 변 80 cm 삼각형
print(f"삼각형 뒤 위치: ({round(drone.get_pos_x())}, {round(drone.get_pos_y())}), 방향 {drone.get_angle_z()}도")

drone.land()
drone.close()


# ----- 실행 결과 (가상 드론) -----
# 사각형 뒤 위치: (0, 0), 방향 0.0도
# 삼각형 뒤 위치: (0, 0), 방향 0.0도
