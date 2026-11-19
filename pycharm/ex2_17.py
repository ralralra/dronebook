# 예제 2-17. 설명이 빠진 함수 찾기
# 2-4 모듈과 패키지 구성
# 먼저 ex2_15.py 를 실행해야 합니다. 그 예제가 만든 파일을 이 예제가 읽습니다.

import mydrone

print("[mydrone 이 제공하는 기능]")
for 이름 in dir(mydrone):
    if 이름.startswith("_"):
        continue
    값 = getattr(mydrone, 이름)
    if callable(값):
        설명 = (값.__doc__ or "!! 설명 없음").strip().splitlines()[0]
        print(f"  {이름:8s} {설명}")


# ----- 실행 결과 (가상 드론) -----
# [mydrone 이 제공하는 기능]
#   목표로이동    현재 위치에서 (x, y) cm 로 이동하고 도착 좌표를 돌려준다.
#   안전착륙     !! 설명 없음
#   점검       배터리와 비행 상태를 확인하여 (통과 여부, 이유)를 돌려준다.
