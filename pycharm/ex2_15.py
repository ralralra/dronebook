# 예제 2-15. 우리 모둠 패키지 만들기
# 2-4 모듈과 패키지 구성

import os
os.makedirs("mydrone", exist_ok=True)

파일들 = {
"mydrone/__init__.py": '''"""mydrone - 우리 모둠의 드론 라이브러리"""
from .check import 점검, 안전착륙
from .path import 목표로이동
''',
"mydrone/check.py": '''"""비행 전 점검과 안전 착륙"""

def 점검(drone, 최소배터리=50):
    """배터리와 비행 상태를 확인하여 (통과 여부, 이유)를 돌려준다."""
    if drone.get_battery() < 최소배터리:
        return False, f"배터리 {drone.get_battery()} % 가 기준 {최소배터리} % 미만"
    if drone.get_flight_state().name != "Ready":
        return False, "이미 비행 중"
    return True, "통과"

def 안전착륙(drone):
    drone.land()
    return drone.get_battery()
''',
"mydrone/path.py": '''"""경로 비행"""
import math

def 목표로이동(drone, x, y, 속도=0.5):
    """현재 위치에서 (x, y) cm 로 이동하고 도착 좌표를 돌려준다."""
    dx = (x - drone.get_pos_x()) / 100
    dy = (y - drone.get_pos_y()) / 100
    drone.move_distance(dx, dy, 0, 속도)
    return round(drone.get_pos_x()), round(drone.get_pos_y())
''',
}
for 이름, 내용 in 파일들.items():
    with open(이름, "w", encoding="utf-8") as f:
        f.write(내용)
print("만든 파일:", list(파일들))


# ----- 실행 결과 (가상 드론) -----
# 만든 파일: ['mydrone/__init__.py', 'mydrone/check.py', 'mydrone/path.py']
