# 예제 2-3. 무슨 일이 있어도 착륙하기
# 2-1 함수와 예외 처리

from drone_sim import *

def 전진(drone, 거리):
    """교실 안전 기준(1~300 cm)을 벗어난 거리는 거부한다."""
    if not (1 <= 거리 <= 300):
        raise ValueError(f"전진 거리는 1~300 cm 여야 합니다. (받은 값: {거리})")
    drone.move_forward(거리)

drone = Drone()
drone.pair()
try:
    drone.takeoff()
    전진(drone, 100)
    전진(drone, 900)          # 여기서 오류가 난다
    전진(drone, 100)          # 실행되지 않는다
except ValueError as e:
    print("[오류]", e)
else:
    print("오류 없이 모두 수행하였습니다.")
finally:
    print("[finally] 안전을 위해 착륙합니다.")
    drone.land()
    drone.close()

print("비행 상태:", drone.get_flight_state().name)


# ----- 실행 결과 (가상 드론) -----
# [가상] 드론에 연결되었습니다. 배터리 100 %
# [가상] 이륙. 고도 약 80 cm
# [가상] 앞으로 100cm
# [오류] 전진 거리는 1~300 cm 여야 합니다. (받은 값: 900)
# [finally] 안전을 위해 착륙합니다.
# [가상] 착륙
# [가상] 연결을 닫았습니다.
# 비행 상태: Ready
