# 예제 4-1. 명령이 실제로 있는지 확인하기
# 4-1 AI 활용 코드 작성과 검증
# 필요한 라이브러리: codrone-edu

from codrone_edu.drone import Drone      # 실기체 라이브러리 (드론을 연결하지 않아도 된다)

for 이름 in ["get_front_range", "get_distance", "set_throttle", "set_power", "get_angle_x", "get_tilt"]:
    print(f"{이름:16s} {'있음' if hasattr(Drone, 이름) else '없음 ← 지어낸 명령일 수 있음'}")


# ----- 실행 결과 (가상 드론) -----
# get_front_range  있음
# get_distance     없음 ← 지어낸 명령일 수 있음
# set_throttle     있음
# set_power        없음 ← 지어낸 명령일 수 있음
# get_angle_x      있음
# get_tilt         없음 ← 지어낸 명령일 수 있음
