# 예제 4-4. 안전장치를 더한 코드
# 4-1 AI 활용 코드 작성과 검증

from drone_sim import *
import statistics

def 안전전진(drone, 남길거리=50, 한걸음=30, 최대반복=10, 최소배터리=40):
    """앞 장애물까지 남길거리(cm)를 남기고 멈춘다.
    반복 횟수, 배터리, 센서 측정 실패에 제한을 두어 멈추지 않는 일이 없게 한다.
    돌려주는 값: 멈춘 까닭(문자열)"""
    결과 = "알 수 없음"
    try:
        drone.takeoff()
        for 회 in range(최대반복):                          # [수정 1] 횟수 제한
            if drone.get_battery() < 최소배터리:            # [수정 2] 배터리 제한
                결과 = "배터리 부족으로 중단"
                break
            거리 = statistics.median([drone.get_front_range() for _ in range(3)])
            if 거리 > 150:                                  # [수정 3] 측정 실패 처리
                결과 = "앞 거리를 잴 수 없어 중단"
                break
            if 거리 <= 남길거리:
                결과 = f"목표 도달 (앞 {거리} cm)"
                break
            drone.move_forward(min(한걸음, 거리 - 남길거리))   # [수정 4] 지나치지 않게
        else:
            결과 = "최대 반복 횟수 도달"                    # [수정 5] 끝까지 간 경우
    finally:
        drone.land()
    return 결과

for 벽 in [140, None]:
    drone = Drone(verbose=False)
    drone.pair()
    drone.sim_set_obstacle(벽)
    print(f"벽 {벽} → {안전전진(drone)}, 멈춘 위치 x = {round(drone.get_pos_x())} cm")


# ----- 실행 결과 (가상 드론) -----
# 벽 140 → 목표 도달 (앞 49.9 cm), 멈춘 위치 x = 91 cm
# 벽 None → 앞 거리를 잴 수 없어 중단, 멈춘 위치 x = 0 cm
