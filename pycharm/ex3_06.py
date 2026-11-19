# 예제 3-6. 바닥 색에 따라 동작 정하기
# 3-2 자세·기압·색상 센서 활용

from drone_sim import *

동작표 = {
    "green": ("전진", (0, 255, 0)),
    "yellow": ("왼쪽회전", (255, 255, 0)),
    "red": ("정지", (255, 0, 0)),
}

drone = Drone(verbose=False)
drone.pair()

for 바닥색 in ["green", "yellow", "light blue", "red"]:
    drone.sim_set_floor(바닥색)                   # 가상 드론 전용: 바닥 색 바꾸기
    앞색 = drone.get_front_color()
    if 앞색 not in 동작표:
        print(f"바닥 '{앞색}' → 모르는 색이므로 이번 칸은 건너뜁니다.")
        continue
    동작, (r, g, b) = 동작표[앞색]
    drone.set_drone_LED(r, g, b, 100)
    print(f"바닥 '{앞색}' → {동작}")
    if 동작 == "정지":
        break

drone.close()


# ----- 실행 결과 (가상 드론) -----
# 바닥 'green' → 전진
# 바닥 'yellow' → 왼쪽회전
# 바닥 'light blue' → 모르는 색이므로 이번 칸은 건너뜁니다.
# 바닥 'red' → 정지
