# 예제 2-16. 만든 패키지 쓰기
# 2-4 모듈과 패키지 구성
# 먼저 ex2_15.py 를 실행해야 합니다. 그 예제가 만든 파일을 이 예제가 읽습니다.

from drone_sim import *
import mydrone

drone = Drone(verbose=False)
drone.pair()

통과, 이유 = mydrone.점검(drone, 최소배터리=60)
print("점검:", 이유)
if 통과:
    drone.takeoff()
    for x, y in [(120, 0), (120, 80), (0, 0)]:
        print("  도착:", mydrone.목표로이동(drone, x, y))
    print("남은 배터리:", mydrone.안전착륙(drone), "%")
drone.close()


# ----- 실행 결과 (가상 드론) -----
# 점검: 통과
#   도착: (120, 0)
#   도착: (120, 80)
#   도착: (0, 0)
# 남은 배터리: 96 %
