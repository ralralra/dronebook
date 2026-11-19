# 예제 2-12. 이륙 전에 스스로 점검하는 드론
# 2-3 클래스·객체와 상속

from drone_sim import *

class 안전드론(Drone):                        # Drone 을 물려받는다
    def __init__(self, 최소배터리=50):
        super().__init__()                    # 부모의 준비 과정을 그대로 실행
        self.최소배터리 = 최소배터리           # 새로 더한 속성
        self.이동기록 = []

    def takeoff(self):                        # 같은 이름으로 다시 정의
        if self.get_battery() < self.최소배터리:
            self.set_drone_LED(255, 0, 0, 100)
            print(f"[안전드론] 배터리 {self.get_battery()} % - 이륙하지 않습니다.")
            return False
        self.set_drone_LED(0, 255, 0, 100)
        super().takeoff()                     # 부모의 takeoff 를 그대로 실행
        return True

    def 기록하며전진(self, 거리):              # 새로 더한 기능
        self.move_forward(거리)
        self.이동기록.append((round(self.get_pos_x()), round(self.get_pos_y())))

drone = 안전드론(최소배터리=60)
drone.pair()
if drone.takeoff():
    drone.기록하며전진(100)
    drone.turn_left(90)                       # 물려받은 기능
    drone.기록하며전진(50)
    drone.land()
print("이동 기록:", drone.이동기록)
drone.close()


# ----- 실행 결과 (가상 드론) -----
# [가상] 드론에 연결되었습니다. 배터리 100 %
# [LED] 드론 초록 (밝기 100)
# [가상] 이륙. 고도 약 80 cm
# [가상] 앞으로 100cm
# [가상] 왼쪽으로 90도 회전
# [가상] 앞으로 50cm
# [가상] 착륙
# 이동 기록: [(100, 0), (100, 50)]
# [가상] 연결을 닫았습니다.
