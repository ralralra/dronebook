# 예제 4-2. AI가 만들었다고 가정한 코드
# 4-1 AI 활용 코드 작성과 검증

from drone_sim import *
import statistics

def 안전전진(drone):
    """앞 장애물까지 50 cm를 남기고 멈춘다."""
    try:
        drone.takeoff()
        while True:                              # 목표에 닿을 때까지 반복
            거리 = statistics.median([drone.get_front_range() for _ in range(3)])
            if 거리 <= 50:
                print(f"  정지. 앞 {거리} cm")
                break
            drone.move_forward(30)
    finally:
        drone.land()

drone = Drone(verbose=False)
drone.pair()
drone.sim_set_obstacle(140)                      # 가상 드론 전용: 앞 140 cm 에 벽
안전전진(drone)
print(f"멈춘 위치 x = {round(drone.get_pos_x())} cm")


# ----- 실행 결과 (가상 드론) -----
#   정지. 앞 20.89 cm
# 멈춘 위치 x = 120 cm
