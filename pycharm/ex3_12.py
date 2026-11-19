# 예제 3-12. 비례 제어로 목표 고도 맞추기
# 3-4 피드백과 비례 제어

from drone_sim import *

목표고도 = 120
Kp = 1.0

drone = Drone(verbose=False)
drone.pair()
drone.takeoff()

print(f"{'시간':>4} {'고도':>7} {'오차':>7} {'출력':>5}")
for i in range(40):
    현재 = drone.get_height()
    오차 = 목표고도 - 현재
    출력 = max(-100, min(100, round(Kp * 오차)))    # 출력은 -100~100
    drone.set_throttle(출력)
    drone.move(0.1)
    if i % 5 == 0:
        print(f"{i * 0.1:>4.1f} {현재:>8.1f} {오차:>7.1f} {출력:>5}")
drone.reset_move_values()
print(f"최종 고도 {drone.get_height()} cm (목표 {목표고도} cm)")
drone.land()


# ----- 실행 결과 (가상 드론) -----
#   시간      고도      오차    출력
#  0.0     78.6    41.4    41
#  0.5     90.2    29.8    30
#  1.0    106.0    14.0    14
#  1.5    112.1     7.9     8
#  2.0    117.1     2.9     3
#  2.5    117.7     2.3     2
#  3.0    120.4    -0.4     0
#  3.5    119.5     0.5     1
# 최종 고도 120.06 cm (목표 120 cm)
