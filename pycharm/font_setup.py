"""font_setup.py - 그래프에 한글이 깨지지 않도록 글꼴을 정해 주는 모듈
그래프를 그리는 예제에서 import font_setup 한 줄만 적으면 된다.
코랩에는 한글 글꼴이 없으므로, 처음 한 번 나눔고딕을 설치한다.
"""
import os
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

NANUM = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"

# 1) 코랩이면 나눔고딕을 설치해서 등록한다
if os.path.exists("/content") and not os.path.exists(NANUM):
    os.system("apt-get -qq install fonts-nanum > /dev/null")
if os.path.exists(NANUM):
    fm.fontManager.addfont(NANUM)

# 2) 운영체제마다 들어 있는 한글 글꼴이 다르므로, 있는 것을 찾아 쓴다
candidates = ["NanumGothic", "Malgun Gothic", "AppleGothic", "Noto Sans CJK KR"]
installed = {f.name for f in fm.fontManager.ttflist}
for name in candidates:
    if name in installed:
        plt.rcParams["font.family"] = name
        break
else:
    print("한글 글꼴을 찾지 못했습니다. 그래프의 한글이 깨질 수 있습니다.")

plt.rcParams["axes.unicode_minus"] = False   # 음수 기호가 깨지지 않도록
