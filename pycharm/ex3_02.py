# 예제 3-2. 장애물 앞에서 멈추기
# 3-1 거리·고도 센서 활용

from drone_sim import *

안전거리 = 50          # 이보다 가까워지면 멈춘다
한걸음 = 20

drone = Drone(verbose=False)
drone.pair()
drone.takeoff()
drone.sim_set_obstacle(140)           # 가상 드론 전용

for 걸음 in range(1, 11):
    거리 = drone.get_front_range()
    if 거리 < 안전거리:
        print(f"  정지! 장애물까지 {거리} cm (안전거리 {안전거리} cm)")
        break
    print(f"  {걸음}걸음째 - 앞 {거리} cm, {한걸음} cm 전진")
    drone.move_forward(한걸음)

drone.land()
print(f"멈춘 위치 x = {round(drone.get_pos_x())} cm")


# ----- 실행 결과 (가상 드론) -----
#   1걸음째 - 앞 138.61 cm, 20 cm 전진
#   2걸음째 - 앞 119.89 cm, 20 cm 전진
#   3걸음째 - 앞 99.64 cm, 20 cm 전진
#   4걸음째 - 앞 80.08 cm, 20 cm 전진
#   5걸음째 - 앞 59.21 cm, 20 cm 전진
#   정지! 장애물까지 39.48 cm (안전거리 50 cm)
# 멈춘 위치 x = 100 cm
