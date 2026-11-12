"""drone_sim.py - 수업용 가상 드론 모듈
AI 드론 코딩1 교과서의 모든 예제는 이 모듈로 실행할 수 있다.
속도와 바람을 바꾸어 가며 같은 비행을 되풀이해 볼 수 있다.
"""
import csv, math


class Drone:
    def __init__(self, battery=100, speed=50, wind=0, log_file="flight_log.csv"):
        self.battery = float(battery)  # 배터리 잔량(%)
        self.speed = speed             # 비행 속도(cm/s)
        self.wind = wind               # 풍속(m/s)
        self.height = 0                # 고도(cm)
        self.x = 0                     # 가로 위치(cm)
        self.y = 0                     # 세로 위치(cm)
        self.angle = 0                 # 방향(도, 0=북)
        self.flying = False
        self.time = 0                  # 비행 시간(초)
        self.log_file = log_file
        self.log = []
        self._record("준비")

    # ---------- 내부 기능 ----------
    def _record(self, action):
        self.log.append({"시간": round(self.time, 1), "동작": action,
                         "고도": self.height, "x": self.x, "y": self.y,
                         "방향": self.angle, "배터리": self.get_battery()})

    def _use(self, seconds, power):
        self.time += seconds
        self.battery = max(0, self.battery - power)

    # ---------- 학생이 사용하는 기능 ----------
    def connect(self):
        print("드론에 연결되었습니다. 배터리:", self.get_battery(), "%")
        self._record("연결")

    def takeoff(self, height=100):
        if self.battery < 20:
            print("배터리가 부족하여 이륙할 수 없습니다.")
            return
        self.height = height
        self.flying = True
        self._use(3, 2)
        print("이륙: 고도", self.height, "cm")
        self._record("이륙")

    def land(self):
        self.height = 0
        self.flying = False
        self._use(3, 1)
        print("착륙하였습니다.")
        self._record("착륙")

    def move_forward(self, distance):
        rad = math.radians(self.angle)
        drift = self.wind * 2                      # 바람에 옆으로 밀리는 정도(cm)
        self.x += round(distance * math.sin(rad) + drift)
        self.y += round(distance * math.cos(rad))
        self._use(distance / self.speed, distance * 0.02 * (1 + self.wind * 0.1))
        print("전진:", distance, "cm")
        self._record("전진")

    def turn_right(self, degree):
        self.angle = (self.angle + degree) % 360
        self._use(degree / 90, degree * 0.005)
        print("우회전:", degree, "도")
        self._record("우회전")

    def get_battery(self):
        return round(float(self.battery), 1)

    def get_height(self):
        return self.height

    def get_position(self):
        return (self.x, self.y)

    def save_log(self):
        with open(self.log_file, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=list(self.log[0].keys()))
            writer.writeheader()
            writer.writerows(self.log)
        print("비행 기록을", self.log_file, "에 저장하였습니다.")
