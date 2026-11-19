# 예제 4-14. 검토할 코드
# 4-4 AI 활용 코드 검토와 문서화
# 필요한 라이브러리: codrone-edu
# 실기체가 있어야 실행됩니다. 드론과 조종기를 연결한 뒤 실행하세요.

from codrone_edu.drone import *

def f(d, t):
    d.takeoff()
    while True:
        e = t - d.get_height()
        d.set_throttle(e * 6)
        d.move(0.1)
        if abs(e) < 1:
            break
    return d.get_height()

drone = Drone()
drone.pair()
print(f(drone, 120))
