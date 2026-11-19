# 예제 1-3. 배터리 상태를 빛과 소리로 나타내기
# 1-1 드론 연결과 신호 출력

from drone_sim import *

drone = Drone()
drone.pair()

battery = drone.get_battery()
if battery >= 70:
    drone.set_drone_LED(0, 255, 0, 100)      # 초록: 충분함
    drone.drone_buzzer(Note.C5, 300)
elif battery >= 30:
    drone.set_drone_LED(255, 255, 0, 100)    # 노랑: 주의
    drone.drone_buzzer(Note.E4, 300)
else:
    drone.set_drone_LED(255, 0, 0, 100)      # 빨강: 위험
    drone.drone_buzzer(Note.C4, 1000)

print("배터리", battery, "% 상태를 신호로 알렸습니다.")
drone.close()


# ----- 실행 결과 (가상 드론) -----
# [가상] 드론에 연결되었습니다. 배터리 100 %
# [LED] 드론 초록 (밝기 100)
# [소리] 드론 523Hz 300ms
# 배터리 100 % 상태를 신호로 알렸습니다.
# [가상] 연결을 닫았습니다.
