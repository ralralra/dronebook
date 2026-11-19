# 예제 1-2. 연결 없이 이륙을 시도하면
# 1-1 드론 연결과 신호 출력
# 이 예제는 오류가 나는 것이 정상입니다. 연결하지 않고 명령을 내리면 어떻게 되는지 확인합니다.

from drone_sim import *

drone = Drone()
drone.takeoff()


# ----- 실행 결과 (가상 드론) -----
# drone_sim.NotConnectedError: 드론에 연결되어 있지 않습니다. drone.pair() 를 먼저 실행하세요.
