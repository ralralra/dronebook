# 예제 2-14. 모듈 만들고 불러오기
# 2-4 모듈과 패키지 구성

# (1) path_tools.py 파일을 만든다 (파이참에서는 직접 만들어 저장)
코드 = '''"""path_tools.py - 경로 계산에 쓰는 도구"""
import math

def 총거리(경유지):
    """경유지를 차례로 이을 때의 전체 거리(cm)를 구한다."""
    합 = 0
    for i in range(len(경유지) - 1):
        합 += math.dist(경유지[i], 경유지[i + 1])
    return round(합, 1)

def 각도(현재, 목표):
    """목표를 바라보는 각도(도, 앞 0, 왼쪽 +)를 구한다."""
    dx, dy = 목표[0] - 현재[0], 목표[1] - 현재[1]
    return round(math.degrees(math.atan2(dy, dx)), 1)
'''
with open("path_tools.py", "w", encoding="utf-8") as f:
    f.write(코드)

# (2) 같은 폴더의 다른 파일에서 불러다 쓴다
import path_tools

경유지 = [(0, 0), (150, 0), (150, 100), (0, 0)]
print("총 거리:", path_tools.총거리(경유지), "cm")
print("각도   :", path_tools.각도((0, 0), (100, 100)), "도")
print("설명   :", path_tools.총거리.__doc__)


# ----- 실행 결과 (가상 드론) -----
# 총 거리: 430.3 cm
# 각도   : 45.0 도
# 설명   : 경유지를 차례로 이을 때의 전체 거리(cm)를 구한다.
