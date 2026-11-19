# 예제 2-2. 비행 결과를 두 값으로 돌려받기
# 2-1 함수와 예외 처리

from drone_sim import *

def 사각비행결과(변길이, 바람=0):
    """사각형 비행을 하고 (출발점과의 거리, 남은 배터리)를 돌려준다."""
    drone = Drone(verbose=False)
    drone.sim_set_wind(바람)                  # 가상 드론 전용
    drone.pair()
    drone.takeoff()
    for i in range(4):
        drone.move_forward(변길이)
        drone.turn_left(90)
    x, y = drone.get_pos_x(), drone.get_pos_y()
    drone.land()
    drone.close()
    오차 = round((x ** 2 + y ** 2) ** 0.5, 1)
    return 오차, drone.get_battery()

for 바람 in [0, 2]:
    오차, 배터리 = 사각비행결과(150, 바람)
    print(f"풍속 {바람} m/s → 출발점과의 거리 {오차} cm, 남은 배터리 {배터리} %")


# ----- 실행 결과 (가상 드론) -----
# 풍속 0 m/s → 출발점과의 거리 0.0 cm, 남은 배터리 94 %
# 풍속 2 m/s → 출발점과의 거리 53.6 cm, 남은 배터리 93 %
