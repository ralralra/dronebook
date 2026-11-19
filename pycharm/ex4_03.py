# 예제 4-3. 벽이 측정 범위 밖에 있을 때
# 4-1 AI 활용 코드 작성과 검증

from drone_sim import *
import statistics

drone = Drone(verbose=False)
drone.pair()
drone.takeoff()
drone.sim_set_obstacle(None)                     # 측정 범위 안에 벽이 없다

for 회 in range(1, 21):                          # 책에서는 20번으로 제한하여 확인한다
    거리 = statistics.median([drone.get_front_range() for _ in range(3)])
    if 거리 <= 50:
        break
    drone.move_forward(30)
    if 회 % 5 == 0:
        print(f"  {회}회 - 앞 {거리} cm, 지금까지 {round(drone.get_pos_x())} cm 전진, 배터리 {drone.get_battery()} %")
drone.land()


# ----- 실행 결과 (가상 드론) -----
#   5회 - 앞 999 cm, 지금까지 150 cm 전진, 배터리 98 %
#   10회 - 앞 999 cm, 지금까지 300 cm 전진, 배터리 97 %
#   15회 - 앞 999 cm, 지금까지 450 cm 전진, 배터리 96 %
#   20회 - 앞 999 cm, 지금까지 600 cm 전진, 배터리 96 %
