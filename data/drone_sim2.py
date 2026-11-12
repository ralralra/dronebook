"""drone_sim2.py - 수업용 가상 드론 모듈 (AI 드론 코딩2)
'AI 드론 코딩1'의 drone_sim 에 센서, 예외 처리, 피드백 제어 기능을 더한 것이다.
"""
import csv, math, random


# ───────── 예외 ─────────
class DroneError(Exception):
    """드론을 다루는 중에 생기는 문제"""


class NotConnectedError(DroneError):
    """연결하지 않고 명령을 내렸을 때"""


class LowBatteryError(DroneError):
    """배터리가 모자랄 때"""


class Drone:
    def __init__(self, battery=100, speed=50, wind=0, seed=None,
                 log_file="flight_log.csv"):
        self.battery = float(battery)
        self.speed = speed
        self.wind = wind
        self.height = 0          # 고도(cm)
        self.x = 0               # 가로 위치(cm)
        self.y = 0               # 세로 위치(cm)
        self.angle = 0           # 방향(도)
        self.power = 0           # 상승 출력(-100 ~ 100)
        self.vz = 0              # 수직 속도
        self._delay = [0.0, 0.0, 0.0]   # 명령이 모터에 전해지기까지의 지연
        self.time = 0            # 비행 시간(초)
        self.flying = False
        self.connected = False
        self.log_file = log_file
        self.log = []
        self._rng = random.Random(seed if seed is not None else 2)
        self.obstacle = 180      # 앞쪽 장애물까지의 거리(cm)
        self.floor = "white"     # 바닥 색
        self._record("준비")

    # ───────── 내부 기능 ─────────
    def _record(self, action):
        self.log.append({"시간": round(self.time, 1), "동작": action,
                         "고도": round(self.height, 1), "x": self.x, "y": self.y,
                         "방향": self.angle, "배터리": self.get_battery()})

    def _use(self, seconds, power):
        self.time += seconds
        self.battery = max(0, self.battery - power)

    def _need_connection(self):
        if not self.connected:
            raise NotConnectedError("드론에 연결되어 있지 않습니다. connect() 를 먼저 실행하세요.")

    # ───────── 연결과 기본 비행 ─────────
    def connect(self):
        self.connected = True
        print("연결됨. 배터리", self.get_battery(), "%")
        self._record("연결")

    def beep(self, times=1):
        """소리로 상태를 알린다."""
        self._need_connection()
        print("삑! " * times)

    def set_light(self, color):
        """빛으로 상태를 알린다."""
        self._need_connection()
        print(f"[LED] {color}")

    def takeoff(self, height=100):
        self._need_connection()
        if self.battery < 20:
            raise LowBatteryError(f"배터리가 {self.get_battery()} % 로 부족합니다.")
        self.height = height
        self.flying = True
        self._use(3, 2)
        print("이륙. 고도", self.height, "cm")
        self._record("이륙")

    def land(self):
        self._need_connection()
        self.height = 0
        self.flying = False
        self._use(3, 1)
        print("착륙")
        self._record("착륙")

    def emergency_stop(self):
        """비상 정지. 모터를 즉시 멈춘다."""
        self.flying = False
        self.power = 0
        self.vz = 0
        self.height = 0
        print("[비상 정지] 모터를 멈추었습니다.")
        self._record("비상정지")

    # ───────── 이동 ─────────
    def move_forward(self, distance):
        self._need_connection()
        if not isinstance(distance, (int, float)):
            raise TypeError("거리는 숫자여야 합니다.")
        if distance <= 0 or distance > 500:
            raise ValueError(f"거리는 1~500 cm 사이여야 합니다. (받은 값: {distance})")
        rad = math.radians(self.angle)
        self.x += round(distance * math.sin(rad) + self.wind * 2)
        self.y += round(distance * math.cos(rad))
        self.obstacle = max(20, self.obstacle - distance)
        self._use(distance / self.speed, distance * 0.02 * (1 + self.wind * 0.1))
        print("전진", distance, "cm")
        self._record("전진")

    def turn_right(self, degree):
        self._need_connection()
        self.angle = (self.angle + degree) % 360
        self._use(degree / 90, degree * 0.005)
        print("우회전", degree, "도")
        self._record("우회전")

    def go_to(self, x, y):
        """목표 좌표로 곧바로 이동한다."""
        self._need_connection()
        distance = math.dist((self.x, self.y), (x, y))
        self.x, self.y = x, y
        self._use(distance / self.speed, distance * 0.02)
        print(f"이동 → ({x}, {y})")
        self._record("이동")

    # ───────── 센서 ─────────
    def _noise(self, size):
        return self._rng.uniform(-size, size)

    def get_distance(self):
        """앞쪽 장애물까지의 거리(cm). 측정값에는 오차가 있다."""
        self._need_connection()
        return round(self.obstacle + self._noise(3), 1)

    def get_height(self):
        """고도(cm)"""
        return round(self.height + self._noise(1.5), 1)

    def get_tilt(self):
        """기울기(도). (앞뒤, 좌우)"""
        self._need_connection()
        shake = self.wind * 1.5
        return (round(self._noise(2 + shake), 1), round(self._noise(2 + shake), 1))

    def get_pressure(self):
        """기압(hPa). 고도가 높을수록 낮아진다."""
        self._need_connection()
        return round(1013.25 - self.height * 0.12 + self._noise(0.3), 2)

    def get_color(self):
        """아래쪽 바닥의 색"""
        self._need_connection()
        return self.floor

    def set_floor(self, color):
        """(수업용) 바닥 색을 바꾼다."""
        self.floor = color

    def set_obstacle(self, distance):
        """(수업용) 앞쪽 장애물까지의 거리를 정한다."""
        self.obstacle = distance

    # ───────── 피드백 제어 ─────────
    def set_power(self, power):
        """상승 출력을 정한다. 0이면 제자리, 양수면 상승, 음수면 하강."""
        self.power = max(-100, min(100, power))

    def step(self, dt=0.1):
        """시간을 dt 초 만큼 진행시킨다.
        실제 드론처럼 명령이 모터에 전해지기까지 시간이 걸리고, 기체에 관성이 있다."""
        self._delay.append(self.power)
        applied = self._delay.pop(0)          # 세 번 전에 내린 명령이 지금 반영된다
        self.vz = self.vz * 0.6 + applied * 5 * dt
        self.height = max(0, self.height + self.vz * dt)
        self._use(dt, abs(applied) * 0.002 + 0.01)
        return self.get_height()

    # ───────── 상태와 기록 ─────────
    def get_battery(self):
        return round(float(self.battery), 1)

    def get_position(self):
        return (self.x, self.y)

    def status(self):
        return {"연결": self.connected, "비행중": self.flying,
                "고도": self.get_height(), "배터리": self.get_battery()}

    def save_log(self):
        with open(self.log_file, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=list(self.log[0].keys()))
            writer.writeheader()
            writer.writerows(self.log)
        print("비행 기록 저장:", self.log_file)
