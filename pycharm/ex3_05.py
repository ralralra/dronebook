# 예제 3-5. 기압과 고도의 관계 확인하기
# 3-2 자세·기압·색상 센서 활용

from drone_sim import *

drone = Drone(verbose=False)
drone.pair()
지상기압 = drone.get_pressure()
print(f"지상 기압 {지상기압} Pa")

drone.takeoff()
print(f"{'거리 센서 고도':>10} {'기압(Pa)':>11} {'기압 차':>8} {'기압으로 구한 고도':>12}")
for 단계 in range(3):
    기압 = drone.get_pressure()
    차 = 지상기압 - 기압
    print(f"{drone.get_height():>12.1f} {기압:>12.2f} {차:>8.2f} {차 / 0.12:>14.1f}")
    drone.move_distance(0, 0, 0.3, 0.5)        # 30 cm 올라간다
drone.land()


# ----- 실행 결과 (가상 드론) -----
# 지상 기압 101325.46 Pa
#   거리 센서 고도      기압(Pa)     기압 차   기압으로 구한 고도
#         79.9    101314.93    10.53           87.8
#        111.2    101311.68    13.78          114.8
#        139.2    101308.26    17.20          143.3
