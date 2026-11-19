# 예제 2-18. 조건을 파일 이름에 담아 기록 저장하기
# 2-5 비행 기록 관리 및 분석

from drone_sim import *
import csv, time

def 기록(drone, 기록장, 동작, 시작시각):
    기록장.append({
        "시간": round(time.time() - 시작시각, 2),
        "동작": 동작,
        "x": round(drone.get_pos_x(), 1),
        "y": round(drone.get_pos_y(), 1),
        "고도": drone.get_height(),
        "배터리": drone.get_battery(),
    })

def 사각비행기록(바람, 파일이름):
    drone = Drone(verbose=False)
    drone.sim_set_wind(바람)                     # 가상 드론 전용
    drone.pair()
    기록장, 시작 = [], time.time()
    drone.takeoff();       기록(drone, 기록장, "이륙", 시작)
    for i in range(4):
        drone.move_forward(200); 기록(drone, 기록장, "전진", 시작)
        drone.turn_left(90);     기록(drone, 기록장, "회전", 시작)
    drone.land();          기록(drone, 기록장, "착륙", 시작)
    drone.close()

    with open(파일이름, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=기록장[0].keys())
        w.writeheader()
        w.writerows(기록장)
    return len(기록장)

for 바람 in [0, 2, 4]:
    이름 = f"flight_wind{바람}.csv"
    줄수 = 사각비행기록(바람, 이름)
    print(f"{이름:18s} {줄수}줄 저장")


# ----- 실행 결과 (가상 드론) -----
# flight_wind0.csv   10줄 저장
# flight_wind2.csv   10줄 저장
# flight_wind4.csv   10줄 저장
