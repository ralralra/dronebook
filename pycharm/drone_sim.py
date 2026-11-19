"""drone_sim.py - 수업용 가상 드론 모듈 ('AI 드론 데이터 코딩'·'AI 드론 지능형 제어' 공용)

실제 기체 없이 CoDrone EDU 파이썬 수업을 할 수 있게 만든 가상 드론이다.
함수 이름과 사용법을 CoDrone EDU 공식 라이브러리(codrone_edu)와 똑같이 맞추었으므로,
가상 드론에서 완성한 프로그램은 첫 줄만 바꾸면 실기체에서 실행된다.

    from drone_sim import *            # 가상 드론
    from codrone_edu.drone import *    # 실기체 (이 줄로 바꾸면 된다)

이 모듈만의 기능에는 모두 sim_ 이 붙어 있다. 실기체로 옮길 때에는 sim_ 줄을 지운다.
    drone.sim_set_wind(4)          바람 세기(m/s)
    drone.sim_set_obstacle(120)    앞쪽 장애물까지 거리(cm)
    drone.sim_set_floor("red")     바닥 색
    drone.sim_save_log()           비행 기록을 CSV로 저장

좌표는 CoDrone EDU와 같다. 이륙한 곳이 원점이고 x는 앞(+)뒤(-), y는 왼쪽(+)오른쪽(-), z는 위(+)이다.
회전 각도는 왼쪽이 +, 오른쪽이 - 이다.

이전 교재의 이름(connect, set_light, beep, get_distance 등)도 당분간 쓸 수 있지만,
실행할 때 실기체 이름을 안내하는 문구가 한 번 나온다.
"""
import csv
import math
import random
import time as _time
from enum import Enum

__all__ = ["Drone", "Note", "ModeFlight", "DroneError", "NotConnectedError", "LowBatteryError"]


# ───────── 예외 (가상 드론 전용. 실기체 라이브러리에는 없다) ─────────
class DroneError(Exception):
    """드론을 다루는 중에 생기는 문제"""


class NotConnectedError(DroneError):
    """pair() 로 연결하지 않고 명령을 내렸을 때"""


class LowBatteryError(DroneError):
    """배터리가 모자라 이륙할 수 없을 때"""


# ───────── 음계 (CoDrone EDU 의 Note 와 같은 쓰임) ─────────
class Note:
    C4, D4, E4, F4, G4, A4, B4 = 262, 294, 330, 349, 392, 440, 494
    C5, D5, E5, F5, G5, A5, B5 = 523, 587, 659, 698, 784, 880, 988


_COLOR_NAMES = {
    (255, 0, 0): "빨강", (0, 255, 0): "초록", (0, 0, 255): "파랑",
    (255, 255, 0): "노랑", (0, 255, 255): "하늘", (255, 0, 255): "보라",
    (255, 255, 255): "흰색", (0, 0, 0): "꺼짐",
}
_LEGACY_COLOR = {"빨강": (255, 0, 0), "초록": (0, 255, 0), "파랑": (0, 0, 255),
                 "노랑": (255, 255, 0), "하늘": (0, 255, 255), "보라": (255, 0, 255),
                 "흰색": (255, 255, 255)}
_FLOOR_COLORS = ["red", "green", "yellow", "blue", "light blue", "purple", "black", "white"]


class ModeFlight(Enum):
    """실기체의 get_flight_state() 가 돌려주는 값과 같은 이름. .name 으로 이름을 꺼낸다."""
    Ready = 16
    TakeOff = 18
    Flight = 19
    Landing = 20

_DT = 0.05          # 계산 간격(초)
_TAKEOFF_CM = 80    # CoDrone EDU 는 평균 80cm 높이로 이륙한다
_SENSOR_MAX = 150   # 거리 센서 측정 한계(cm)


class Drone:
    def __init__(self, battery=100, wind=0, seed=None, log_file="flight_log.csv", verbose=True):
        # 앞의 인자들은 가상 드론 전용이다. 실기체는 Drone() 처럼 비워서 만든다.
        self._rng = random.Random(2 if seed is None else seed)
        self._verbose = verbose
        self._log_file = log_file
        self._warned = set()
        self._paired = False
        self._flying = False
        self._battery = float(battery)
        self._wind = float(wind)
        self._drift = 0.0                 # 기체 자체가 옆으로 흐르는 정도(cm/s), 트림으로 잡는다
        self._trim = [0, 0]               # [roll, pitch]
        self._t = 0.0                     # 비행 시간(초)
        self._x = self._y = self._z = 0.0  # cm
        self._heading = 0.0               # 도, 왼쪽 +
        self._v = [0.0, 0.0, 0.0]         # 앞뒤·좌우·위아래 속도(cm/s)
        self._delay = [[0, 0, 0, 0]] * 3  # 명령이 모터에 전해지기까지의 지연
        self._move = [0, 0, 0, 0]         # roll, pitch, yaw, throttle
        self._obstacle_x = None           # 장애물의 x 좌표(cm)
        self._floor = "white"
        self._led = (0, 0, 0)
        self._p0 = None
        self._press_at = {}
        self.sim_log = []
        self._record("준비")

    # ───────── 내부 기능 ─────────
    def _say(self, msg):
        if self._verbose:
            print(msg)

    def _warn_once(self, key, msg):
        if key not in self._warned:
            self._warned.add(key)
            print(msg)

    def _record(self, action):
        self.sim_log.append({"시간": round(self._t, 2), "동작": action,
                             "x": round(self._x, 1), "y": round(self._y, 1), "z": round(self._z, 1),
                             "방향": round(self._heading, 1), "배터리": round(self._battery, 1),
                             "풍속": self._wind})

    def _need_pair(self):
        if not self._paired:
            raise NotConnectedError("드론에 연결되어 있지 않습니다. drone.pair() 를 먼저 실행하세요.")

    def _need_flying(self, name):
        self._need_pair()
        if not self._flying:
            self._say(f"[가상] 이륙하지 않은 상태라 {name}() 명령을 무시합니다.")
            return False
        return True

    def _noise(self, size):
        return self._rng.uniform(-size, size)

    def _drain(self, seconds, load=0.0):
        """배터리 소모. 정지 비행만 해도 약 8분이면 바닥난다."""
        if self._flying:
            self._battery -= seconds * (0.2 + 0.002 * load + 0.02 * self._wind)
        if self._battery <= 0:
            self._battery = 0
            if self._flying:
                self._say("[가상] 배터리가 다 되어 착륙합니다.")
                self._flying = False
                self._z = 0
                self._record("배터리 방전 착륙")

    def _push(self, seconds):
        """바람과 기체 흐름 때문에 옆(오른쪽, -y)으로 밀리는 거리"""
        gust = 1 + self._rng.uniform(-0.6, 0.6)
        side = (self._wind * 3 * gust + self._drift + self._trim[0] * 0.5) * seconds
        return -side

    def _to_world(self, fwd, left):
        h = math.radians(self._heading)
        return (fwd * math.cos(h) - left * math.sin(h), fwd * math.sin(h) + left * math.cos(h))

    def _cm(self, value, units):
        # 실기체와 같이 cm, m, in, ft 만 받는다. 다른 단위는 오류 문구만 내고 움직이지 않는다.
        table = {"cm": 1, "m": 100, "in": 2.54, "ft": 30.48}
        if units not in table:
            print("Error: Not a valid unit.")
            return None
        return value * table[units]

    def _out(self, value_cm, unit):
        return round(value_cm / {"cm": 1, "m": 100, "mm": 0.1, "in": 2.54}[unit], 2)

    # ───────── 연결 ─────────
    def pair(self, portname=None):
        self._paired = True
        self._say(f"[가상] 드론에 연결되었습니다. 배터리 {self.get_battery()} %")
        self._record("연결")

    def close(self):
        self._paired = False
        self._say("[가상] 연결을 닫았습니다.")
        self._record("연결 종료")

    # ───────── 이륙·착륙 ─────────
    def takeoff(self):
        self._need_pair()
        if self._battery < 20:
            raise LowBatteryError(f"배터리가 {self.get_battery()} % 로 부족하여 이륙할 수 없습니다.")
        self._flying = True
        self._x = self._y = 0.0           # 실기체처럼 이륙할 때 위치가 0이 된다
        self._heading = 0.0
        self._z = _TAKEOFF_CM
        self._v = [0.0, 0.0, 0.0]
        self._delay = [[0, 0, 0, 0]] * 3  # 이전 비행에서 남은 명령을 비운다
        self._t += 2
        self._drain(2, 50)
        self._say(f"[가상] 이륙. 고도 약 {_TAKEOFF_CM} cm")
        self._record("이륙")
        self.hover(1)                     # 실기체도 이륙 뒤 1초 안정화한다

    def land(self):
        self._need_pair()
        self.reset_move_values()
        if self._flying:
            self._t += 2
            self._drain(2, 20)
        self._flying = False
        self._z = 0.0
        self._say("[가상] 착륙")
        self._record("착륙")

    def emergency_stop(self):
        self._need_pair()
        self.reset_move_values()
        self._flying = False
        self._z = 0.0
        self._v = [0.0, 0.0, 0.0]
        self._say("[가상] 비상 정지. 모터를 멈추었습니다.")
        self._record("비상정지")

    def hover(self, duration=0.01):
        if not self._need_flying("hover"):
            return
        steps = max(1, round(duration / _DT))
        for _ in range(steps):
            self._y += self._push(_DT)
            self._t += _DT
            self._drain(_DT)
        self._record("정지비행")

    # ───────── 비행 변수(롤·피치·요·스로틀) ─────────
    def set_roll(self, power):      # + 오른쪽, - 왼쪽
        self._move[0] = max(-100, min(100, power))

    def set_pitch(self, power):     # + 앞, - 뒤
        self._move[1] = max(-100, min(100, power))

    def set_yaw(self, power):       # + 왼쪽으로 회전, - 오른쪽으로 회전
        self._move[2] = max(-100, min(100, power))

    def set_throttle(self, power):  # + 위, - 아래
        self._move[3] = max(-100, min(100, power))

    def get_move_values(self):
        return list(self._move)

    def reset_move_values(self, attempts=3):
        self._move = [0, 0, 0, 0]

    def move(self, duration=None):
        """설정한 비행 변수대로 duration 초 동안 움직인다.
        명령이 모터에 전해지기까지 시간이 걸리고 기체에 관성이 있는 것까지 흉내 낸다."""
        if not self._need_flying("move"):
            return
        if duration is None:
            duration = 1
            self._warn_once("move_none", "[가상] move() 를 시간 없이 부르면 실기체는 계속 움직입니다. 가상 드론은 1초만 움직입니다.")
        steps = max(1, round(duration / _DT))
        for i in range(steps):
            self._delay.append(list(self._move))
            roll, pitch, yaw, thr = self._delay.pop(0)
            target = [pitch * 1.0, -roll * 1.0, thr * 1.0]
            self._v = [v * 0.6 + tv * 0.4 for v, tv in zip(self._v, target)]
            dx, dy = self._to_world(self._v[0] * _DT, self._v[1] * _DT)
            self._x += dx
            self._y += dy + self._push(_DT)
            self._z = max(0.0, self._z + self._v[2] * _DT)
            self._heading = (self._heading + yaw * 1.8 * _DT + 180) % 360 - 180
            self._t += _DT
            self._drain(_DT, abs(roll) + abs(pitch) + abs(yaw) + abs(thr))
            if not self._flying:
                return
            if i % 4 == 3:
                self._record("이동")

    # ───────── 거리 이동과 회전 ─────────
    def _go(self, fwd, left, up, speed, name):
        if not self._need_flying(name):
            return False
        speed = max(0, min(2, speed))     # 실기체처럼 속도는 0~2 m/s 로 잘린다
        if speed == 0:
            raise ZeroDivisionError("speed 가 0 이라 이동 시간을 계산할 수 없습니다.")
        dist = math.sqrt(fwd ** 2 + left ** 2 + up ** 2)
        seconds = dist / (speed * 100)
        dx, dy = self._to_world(fwd, left)
        self._x += dx
        self._y += dy + self._push(seconds)
        self._z = max(0.0, self._z + up)
        self._t += seconds
        self._drain(seconds, speed * 50)
        self._record(name)
        return True

    def move_forward(self, distance, units="cm", speed=0.5):
        d = self._cm(distance, units)
        if d is not None and self._go(d, 0, 0, speed, "move_forward"):
            self._say(f"[가상] 앞으로 {distance}{units}")

    def move_backward(self, distance, units="cm", speed=0.5):
        d = self._cm(distance, units)
        if d is not None and self._go(-d, 0, 0, speed, "move_backward"):
            self._say(f"[가상] 뒤로 {distance}{units}")

    def move_left(self, distance, units="cm", speed=0.5):
        d = self._cm(distance, units)
        if d is not None and self._go(0, d, 0, speed, "move_left"):
            self._say(f"[가상] 왼쪽으로 {distance}{units}")

    def move_right(self, distance, units="cm", speed=0.5):
        d = self._cm(distance, units)
        if d is not None and self._go(0, -d, 0, speed, "move_right"):
            self._say(f"[가상] 오른쪽으로 {distance}{units}")

    def move_distance(self, positionX, positionY, positionZ, velocity):
        """앞(+x)·왼쪽(+y)·위(+z)로 각각 몇 m 움직일지 한꺼번에 정한다."""
        if self._go(positionX * 100, positionY * 100, positionZ * 100, velocity, "move_distance"):
            self._say(f"[가상] 이동 앞 {positionX}m, 왼쪽 {positionY}m, 위 {positionZ}m")

    def turn_left(self, degree=90):
        if not self._need_flying("turn_left"):
            return
        degree = min(int(abs(degree)), 360)   # 실기체처럼 소수점은 버리고 360도까지만
        self._heading = (self._heading + degree + 180) % 360 - 180
        self._t += degree / 90
        self._drain(degree / 90, 30)
        self._say(f"[가상] 왼쪽으로 {degree}도 회전")
        self._record("turn_left")

    def turn_right(self, degree=90):
        if not self._need_flying("turn_right"):
            return
        degree = min(int(abs(degree)), 360)   # 실기체처럼 소수점은 버리고 360도까지만
        self._heading = (self._heading - degree + 180) % 360 - 180
        self._t += degree / 90
        self._drain(degree / 90, 30)
        self._say(f"[가상] 오른쪽으로 {degree}도 회전")
        self._record("turn_right")

    def turn_degree(self, degree, timeout=3, p_value=10):
        """처음 방향을 0으로 하여 degree 방향을 보게 돌린다(왼쪽 +)."""
        if not self._need_flying("turn_degree"):
            return
        turn = abs(degree - self._heading)
        self._heading = (degree + 180) % 360 - 180
        self._t += turn / 90
        self._say(f"[가상] {degree}도 방향으로 회전")
        self._record("turn_degree")

    def flip(self, direction="back"):
        if not self._need_flying("flip"):
            return
        if self._battery < 50:
            self._say("[가상] 배터리가 50% 미만이라 플립을 할 수 없습니다.")
            return
        self._t += 4
        self._drain(4, 150)
        self._say(f"[가상] 플립({direction})")
        self._record("flip")

    # ───────── 정해진 모양 비행 ─────────
    def square(self, speed=60, seconds=1, direction=1):
        for pitch, roll in [(speed, 0), (0, speed * direction), (-speed, 0), (0, -speed * direction)]:
            self.set_pitch(pitch)
            self.set_roll(roll)
            self.move(seconds)
        self.reset_move_values()
        self.hover(1)

    def triangle(self, speed=60, seconds=1, direction=1):
        for k in range(3):
            a = math.radians(120 * k)
            self.set_pitch(round(speed * math.cos(a)))
            self.set_roll(round(speed * math.sin(a) * direction))
            self.move(seconds)
        self.reset_move_values()
        self.hover(1)

    def circle(self, speed=75, direction=1):
        for k in range(12):
            a = math.radians(30 * k)
            self.set_pitch(round(speed * math.cos(a)))
            self.set_roll(round(speed * math.sin(a) * direction))
            self.move(0.4)
        self.reset_move_values()
        self.hover(1)

    # ───────── 트림(기체 흐름 바로잡기) ─────────
    def get_trim(self):
        return list(self._trim)

    def set_trim(self, roll, pitch):
        self._trim = [max(-100, min(100, roll)), max(-100, min(100, pitch))]

    def reset_trim(self):
        self._trim = [0, 0]

    # ───────── 위치 ─────────
    def get_pos_x(self, unit="cm"):
        return self._out(self._x, unit)

    def get_pos_y(self, unit="cm"):
        return self._out(self._y, unit)

    def get_pos_z(self, unit="cm"):
        return self._out(self._z, unit)

    def get_position_data(self, delay=0.01):
        """[시간(초), x(m), y(m), z(m)]"""
        return [round(self._t, 2), round(self._x / 100, 3), round(self._y / 100, 3), round(self._z / 100, 3)]

    # ───────── 거리 센서 ─────────
    def get_height(self, unit="cm"):
        """아래쪽 거리 센서로 잰 고도. 측정 한계를 넘으면 999.9 를 돌려준다."""
        self._need_pair()
        if not self._flying:
            return 0.0
        h = max(0.0, self._z + self._noise(1.5))
        if h > _SENSOR_MAX:
            return 999.9
        return self._out(h, unit)

    def get_bottom_range(self, unit="cm"):
        return self.get_height(unit)

    def get_front_range(self, unit="cm"):
        """앞쪽 거리 센서. 장애물이 없거나 150cm 보다 멀면 999 를 돌려준다."""
        self._need_pair()
        if self._obstacle_x is None or abs(self._heading) > 45:
            return 999
        d = (self._obstacle_x - self._x) / math.cos(math.radians(self._heading))
        if d < 0 or d > _SENSOR_MAX:
            return 999
        return self._out(max(0.0, d + self._noise(1.5)), unit)

    def detect_wall(self, distance=50):
        return self.get_front_range() < distance

    def avoid_wall(self, timeout=2, distance=70):
        """앞으로 가다가 벽이 distance(cm) 안으로 들어오면 멈춘다."""
        if not self._need_flying("avoid_wall"):
            return
        start = self._t
        self.set_pitch(30)
        while self._t - start < timeout and self._flying:
            if self.get_front_range() <= distance:
                break
            self.move(0.1)
        self.reset_move_values()
        self.hover(0.5)

    def keep_distance(self, timeout=2, distance=50):
        """앞 물체와 distance(cm) 를 유지한다(비례 제어)."""
        if not self._need_flying("keep_distance"):
            return
        start = self._t
        while self._t - start < timeout and self._flying:
            front = self.get_front_range()
            error = (front - distance) if front != 999 else 40
            self.set_pitch(max(-40, min(40, round(error * 0.8))))
            self.move(0.1)
        self.reset_move_values()

    # ───────── 자세·기압·온도·색 ─────────
    def get_angle_x(self):   # 롤 방향 기울기(도)
        self._need_pair()
        return round(self._move[0] * 0.15 + self._noise(1 + self._wind * 0.8), 1) if self._flying else 0.0

    def get_angle_y(self):   # 피치 방향 기울기(도)
        self._need_pair()
        return round(self._move[1] * 0.15 + self._noise(1 + self._wind * 0.8), 1) if self._flying else 0.0

    def get_angle_z(self):   # 바라보는 방향(도, 왼쪽 +)
        self._need_pair()
        return round(self._heading, 1)

    def get_pressure(self, unit="Pa"):
        """기압(Pa). 지면 근처에서는 1m 올라갈 때마다 약 12Pa 낮아진다."""
        self._need_pair()
        pa = 101325 - self._z * 0.12 + self._noise(0.5)
        return round(pa if unit == "Pa" else pa / 100, 2)

    def set_initial_pressure(self):
        self._p0 = self.get_pressure()

    def height_from_pressure(self, b=0, m=9.34):
        """set_initial_pressure() 때의 기압과 비교한 높이(cm)"""
        if self._p0 is None:
            self.set_initial_pressure()
        return round((self._p0 - self.get_pressure()) * m + b, 1)

    def get_drone_temperature(self, unit="C"):
        self._need_pair()
        c = 26 + self._t * 0.01 + self._noise(0.3)
        return round({"C": c, "F": c * 9 / 5 + 32, "K": c + 273.15}[unit], 1)

    def get_colors(self, kind="name"):
        """[앞 센서 색, 뒤 센서 색]. 실기체처럼 소문자 영어 이름(red, light blue ...)을 돌려준다."""
        self._need_pair()
        return [self._floor, self._floor]

    def get_front_color(self, kind="name"):
        return self.get_colors(kind)[0]

    def get_back_color(self, kind="name"):
        return self.get_colors(kind)[1]

    def get_battery(self):
        return int(self._battery)          # 실기체처럼 정수(%)로 돌려준다

    def get_flight_state(self):
        """실기체처럼 ModeFlight 값을 돌려준다. 이름은 .name 으로 본다 (예: "Flight")."""
        return ModeFlight.Flight if self._flying else ModeFlight.Ready

    # ───────── 빛과 소리 ─────────
    def set_drone_LED(self, r, g, b, brightness=100):
        self._need_pair()
        self._led = (r, g, b)
        name = _COLOR_NAMES.get((r, g, b), f"RGB({r},{g},{b})")
        self._say(f"[LED] 드론 {name} (밝기 {brightness})")

    def set_controller_LED(self, r, g, b, brightness=100):
        self._need_pair()
        name = _COLOR_NAMES.get((r, g, b), f"RGB({r},{g},{b})")
        self._say(f"[LED] 조종기 {name} (밝기 {brightness})")

    def drone_LED_off(self):
        self.set_drone_LED(0, 0, 0, 0)

    def controller_LED_off(self):
        self.set_controller_LED(0, 0, 0, 0)

    def drone_buzzer(self, note, duration):
        self._need_pair()
        self._say(f"[소리] 드론 {note}Hz {duration}ms")

    def controller_buzzer(self, note, duration):
        self._need_pair()
        self._say(f"[소리] 조종기 {note}Hz {duration}ms")

    # ───────── 조종기 버튼 ─────────
    def _pressed(self, name):
        self._need_pair()
        at = self._press_at.get(name)
        if at is None:
            self._warn_once("btn_" + name, f"[가상] {name} 버튼은 drone.sim_press_after('{name}', 초) 로 눌러 볼 수 있습니다.")
            return False
        if _time.time() >= at:
            del self._press_at[name]
            return True
        return False

    def h_pressed(self):
        return self._pressed("h")

    def up_arrow_pressed(self):
        return self._pressed("up")

    def down_arrow_pressed(self):
        return self._pressed("down")

    def left_arrow_pressed(self):
        return self._pressed("left")

    def right_arrow_pressed(self):
        return self._pressed("right")

    # ───────── 가상 드론 전용 기능 (실기체로 옮길 때 지운다) ─────────
    def sim_set_wind(self, speed):
        """바람 세기(m/s). 바람은 드론을 오른쪽으로 밀고, 세기는 매번 조금씩 흔들린다."""
        self._wind = float(speed)

    def sim_set_drift(self, cm_per_s):
        """기체가 스스로 오른쪽으로 흐르는 정도. set_trim() 의 roll 을 음수로 주면 바로잡힌다."""
        self._drift = float(cm_per_s)

    def sim_set_battery(self, percent):
        self._battery = float(percent)

    def sim_set_obstacle(self, distance):
        """지금 위치 앞쪽 distance(cm) 에 벽을 세운다. None 이면 벽을 없앤다."""
        self._obstacle_x = None if distance is None else self._x + distance

    def sim_set_floor(self, color):
        """바닥 색: red, green, yellow, blue, light blue, purple, black, white"""
        color = color.lower()
        if color not in _FLOOR_COLORS:
            raise ValueError(f"바닥 색은 {_FLOOR_COLORS} 중 하나여야 합니다.")
        self._floor = color

    def sim_press_after(self, button, seconds=0):
        """seconds 초 뒤에 조종기 버튼(h, up, down, left, right)을 누른 것으로 한다."""
        self._press_at[button] = _time.time() + seconds

    def sim_go_to(self, x, y):
        """좌표 (x, y)(cm) 로 곧바로 이동한다. 실기체에서는 move_distance() 로 바꾸어야 한다."""
        dx, dy = x - self._x, y - self._y
        h = math.radians(self._heading)
        fwd = dx * math.cos(h) + dy * math.sin(h)
        left = -dx * math.sin(h) + dy * math.cos(h)
        if self._go(fwd, left, 0, 0.5, "sim_go_to"):
            self._say(f"[가상] ({x}, {y}) 로 이동")

    def sim_save_log(self, filename=None):
        filename = filename or self._log_file
        with open(filename, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=list(self.sim_log[0].keys()))
            w.writeheader()
            w.writerows(self.sim_log)
        self._say(f"[가상] 비행 기록 {len(self.sim_log)}줄을 {filename} 에 저장했습니다.")

    # ───────── 이전 교재 이름 (안내 문구와 함께 실기체 이름으로 연결) ─────────
    def _legacy(self, old, new):
        self._warn_once("legacy_" + old, f"[안내] {old}() 는 이전 교재 이름입니다. 실기체와 같은 {new} 를 쓰세요.")

    def connect(self):
        self._legacy("connect", "pair()")
        self.pair()

    def beep(self, times=1):
        self._legacy("beep", "drone_buzzer(음높이, 시간)")
        for _ in range(times):
            self.drone_buzzer(Note.A4, 200)

    def set_light(self, color):
        self._legacy("set_light", "set_drone_LED(빨강, 초록, 파랑, 밝기)")
        r, g, b = _LEGACY_COLOR.get(color, (255, 255, 255))
        self.set_drone_LED(r, g, b, 100)

    def get_distance(self):
        self._legacy("get_distance", "get_front_range()")
        return self.get_front_range()

    def get_tilt(self):
        self._legacy("get_tilt", "get_angle_y(), get_angle_x()")
        return (self.get_angle_y(), self.get_angle_x())

    def get_color(self):
        self._legacy("get_color", "get_colors()")
        return self.get_colors()[0]

    def get_position(self):
        self._legacy("get_position", "get_pos_x(), get_pos_y()")
        return (round(self._x), round(self._y))

    def status(self):
        self._legacy("status", "get_battery(), get_height(), get_flight_state()")
        return {"연결": self._paired, "비행중": self._flying,
                "고도": self.get_height() if self._paired else 0.0, "배터리": self.get_battery()}

    def save_log(self):
        self._legacy("save_log", "sim_save_log()")
        self.sim_save_log()

    def set_obstacle(self, distance):
        self._legacy("set_obstacle", "sim_set_obstacle()")
        self.sim_set_obstacle(distance)

    def set_floor(self, color):
        self._legacy("set_floor", "sim_set_floor()")
        self.sim_set_floor(color)

    def go_to(self, x, y):
        self._legacy("go_to", "move_distance()")
        self.sim_go_to(x, y)

    def set_power(self, power):
        self._legacy("set_power", "set_throttle()")
        self.set_throttle(power)

    def step(self, dt=0.1):
        self._legacy("step", "move(시간)")
        self.move(dt)
        return self.get_height()
