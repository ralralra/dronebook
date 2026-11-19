# 예제 3-3. 목표 고도와 실제 고도 비교하기
# 3-1 거리·고도 센서 활용

from drone_sim import *

목표고도 = 100
허용오차 = 10

drone = Drone(verbose=False)
drone.pair()
drone.takeoff()

실제 = drone.get_height()
오차 = 목표고도 - 실제
print(f"목표 {목표고도} cm, 실제 {실제} cm, 오차 {round(오차, 1)} cm")
if abs(오차) <= 허용오차:
    print("→ 허용 범위 안입니다.")
elif 오차 > 0:
    print("→ 너무 낮습니다. 고도를 올려야 합니다.")
else:
    print("→ 너무 높습니다. 고도를 낮춰야 합니다.")
drone.land()


# ----- 실행 결과 (가상 드론) -----
# 목표 100 cm, 실제 78.61 cm, 오차 21.4 cm
# → 너무 낮습니다. 고도를 올려야 합니다.
