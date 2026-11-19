# 예제 1-12. 바람이 있을 때의 경로 오차
# 1-3 이동·회전 및 경로 제어

from drone_sim import *
import math

print("풍속(m/s)  도착 위치(x, y)   출발점과의 거리(cm)")
for 바람 in [0, 1, 2, 3]:
    drone = Drone(verbose=False)
    drone.sim_set_wind(바람)              # 가상 드론 전용
    drone.pair()
    drone.takeoff()
    for i in range(4):
        drone.move_forward(100)
        drone.turn_left(90)
    x, y = drone.get_pos_x() + 0.0, drone.get_pos_y() + 0.0
    drone.land()
    print(f"{바람:>6}     ({x:6.1f}, {y:6.1f})   {math.dist((0, 0), (x, y)):10.1f}")


# ----- 실행 결과 (가상 드론) -----
# 풍속(m/s)  도착 위치(x, y)   출발점과의 거리(cm)
#      0     (   0.0,    0.0)          0.0
#      1     (   0.0,  -18.9)         18.9
#      2     (   0.0,  -37.9)         37.9
#      3     (   0.0,  -56.8)         56.8
