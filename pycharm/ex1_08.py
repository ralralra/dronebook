# 예제 1-8. 점검을 거친 안전한 비행
# 1-2 상태 점검과 기본 비행 및 비상 대응

from drone_sim import *

for 시작배터리 in [85, 18]:
    print(f"=== 배터리 {시작배터리}% 로 시작 ===")
    drone = Drone(verbose=False)
    drone.sim_set_battery(시작배터리)      # 가상 드론 전용: 실기체에서는 지운다
    drone.pair()

    if drone.get_battery() < 50:
        drone.set_drone_LED(255, 0, 0, 100)
        print("점검 실패: 배터리가 부족하여 비행을 취소합니다.")
    else:
        drone.set_drone_LED(0, 255, 0, 100)
        drone.takeoff()
        drone.hover(3)
        drone.land()
        print("정상 종료. 남은 배터리", drone.get_battery(), "%")
    drone.close()


# ----- 실행 결과 (가상 드론) -----
# === 배터리 85% 로 시작 ===
# 정상 종료. 남은 배터리 83 %
# === 배터리 18% 로 시작 ===
# 점검 실패: 배터리가 부족하여 비행을 취소합니다.
