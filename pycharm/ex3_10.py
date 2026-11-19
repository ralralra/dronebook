# 예제 3-10. 가까울수록 천천히
# 3-3 센서 데이터 처리와 동작 제어

from drone_sim import *
from collections import deque
import statistics

def 이동거리정하기(남은거리):
    """장애물이 가까울수록 한 번에 가는 거리를 줄인다."""
    if 남은거리 > 120:
        return 40
    elif 남은거리 > 80:
        return 20
    elif 남은거리 > 50:
        return 10
    return 0                                 # 멈춤

drone = Drone(verbose=False)
drone.pair()
drone.takeoff()
drone.sim_set_obstacle(145)

최근값 = deque(maxlen=3)
for i in range(15):
    for _ in range(3):                        # 움직이기 전에 세 번 잰다
        최근값.append(drone.get_front_range())
    거리 = statistics.mean(최근값)
    이동 = 이동거리정하기(거리)
    if 이동 == 0:
        print(f"  앞 {거리:.1f} cm - 정지")
        break
    print(f"  앞 {거리:6.1f} cm - {이동} cm 전진")
    drone.move_forward(이동)
    최근값.clear()                            # 움직였으니 예전 값은 버린다
drone.land()


# ----- 실행 결과 (가상 드론) -----
#   앞  144.0 cm - 40 cm 전진
#   앞  105.3 cm - 20 cm 전진
#   앞   84.1 cm - 20 cm 전진
#   앞   65.7 cm - 10 cm 전진
#   앞   55.9 cm - 10 cm 전진
#   앞 45.4 cm - 정지
