# 예제 2-10. 프로그램 안에서 설명 보기
# 2-2 표준 라이브러리 활용

import statistics
from drone_sim import Drone

print(statistics.median.__doc__.strip().splitlines()[0])
print()
print("[get_front_range]", Drone.get_front_range.__doc__)
print("[get_colors]", Drone.get_colors.__doc__)


# ----- 실행 결과 (가상 드론) -----
# Return the median (middle value) of numeric data.
#
# [get_front_range] 앞쪽 거리 센서. 장애물이 없거나 150cm 보다 멀면 999 를 돌려준다.
# [get_colors] [앞 센서 색, 뒤 센서 색]. 실기체처럼 소문자 영어 이름(red, light blue ...)을 돌려준다.
