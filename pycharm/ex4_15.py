# 예제 4-15. 검토 결과를 반영한 코드
# 4-4 AI 활용 코드 검토와 문서화

from drone_sim import *

def 고도맞추기(drone, 목표고도, Kp=1.0, 허용오차=3, 최대반복=100, 최소배터리=30):
    """비례 제어로 목표 고도(cm)에 맞춘다.

    매개변수:
        drone      : pair() 로 연결한 Drone 객체
        목표고도   : 맞추려는 고도(cm). 아래 거리 센서 범위 안(150 cm 미만)이어야 한다
        Kp         : 비례 상수. 3-4 실험에서 1.0 이 안정적이었다
        허용오차   : 이 안에 들면 도달로 본다(cm)
        최대반복   : 0.1초 단위 반복 횟수의 상한
        최소배터리 : 이 아래로 떨어지면 중단한다(%)
    돌려주는 값:
        (도달 여부, 마지막으로 잰 고도, 멈춘 까닭)
    """
    if not (30 <= 목표고도 < 150):
        raise ValueError(f"목표고도는 30~149 cm 여야 합니다. (받은 값: {목표고도})")
    도달, 까닭, 현재 = False, "최대 반복 횟수 도달", None
    try:
        drone.takeoff()
        for 회 in range(최대반복):
            if drone.get_battery() < 최소배터리:
                까닭 = "배터리 부족"
                break
            현재 = drone.get_height()
            if 현재 > 150:
                까닭 = "고도 측정 실패"
                break
            오차 = 목표고도 - 현재
            if abs(오차) <= 허용오차:
                도달, 까닭 = True, "목표 도달"
                break
            출력 = max(-100, min(100, round(Kp * 오차)))
            drone.set_throttle(출력)
            drone.move(0.1)
        drone.reset_move_values()
        return 도달, 현재, 까닭
    finally:
        drone.land()

drone = Drone(verbose=False)
drone.pair()
print(고도맞추기(drone, 120))
drone.close()


# ----- 실행 결과 (가상 드론) -----
# (True, 117.11, '목표 도달')
