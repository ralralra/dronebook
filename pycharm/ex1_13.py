# 예제 1-13. 배터리에 따라 임무를 줄이는 비행
# 1-4 조건·반복·자료구조를 활용한 비행

from drone_sim import *

구간 = [100, 100, 100, 100, 100]      # 다섯 구간(cm)
복귀기준 = 50                          # 이 아래로 떨어지면 복귀

drone = Drone()
drone.sim_set_battery(52)             # 가상 드론 전용
drone.pair()
drone.takeoff()

완료 = 0
for 번호, 거리 in enumerate(구간, 1):
    if drone.get_battery() < 복귀기준:
        print(f"  배터리 {drone.get_battery()}% - {번호}번 구간부터 포기")
        break
    drone.move_forward(거리)
    완료 = 완료 + 1

drone.land()
print(f"다섯 구간 중 {완료}개 완료")
drone.close()


# ----- 실행 결과 (가상 드론) -----
# [가상] 드론에 연결되었습니다. 배터리 52 %
# [가상] 이륙. 고도 약 80 cm
# [가상] 앞으로 100cm
# [가상] 앞으로 100cm
# [가상] 앞으로 100cm
#   배터리 49% - 4번 구간부터 포기
# [가상] 착륙
# 다섯 구간 중 3개 완료
# [가상] 연결을 닫았습니다.
