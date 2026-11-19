# 예제 2-4. 오류 종류별 대응
# 2-1 함수와 예외 처리

from drone_sim import *

def 안전이륙(배터리, 연결할까):
    drone = Drone(verbose=False)
    drone.sim_set_battery(배터리)        # 가상 드론 전용
    if 연결할까:
        drone.pair()
    try:
        drone.takeoff()
        print("  → 이륙 성공")
        drone.land()
    except LowBatteryError as e:
        print("  → 배터리 문제:", e)
    except NotConnectedError as e:
        print("  → 연결 문제:", e)
    except Exception as e:
        print("  → 그 밖의 문제:", type(e).__name__, e)

print("[정상]")
안전이륙(90, True)
print("[배터리 부족]")
안전이륙(10, True)
print("[연결 안 함]")
안전이륙(90, False)


# ----- 실행 결과 (가상 드론) -----
# [정상]
#   → 이륙 성공
# [배터리 부족]
#   → 배터리 문제: 배터리가 10 % 로 부족하여 이륙할 수 없습니다.
# [연결 안 함]
#   → 연결 문제: 드론에 연결되어 있지 않습니다. drone.pair() 를 먼저 실행하세요.
