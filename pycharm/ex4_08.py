# 예제 4-8. 라이브러리의 색상 데이터 불러오기
# 4-3 센서 데이터 기반 분류 모델 학습 및 평가
# 필요한 라이브러리: codrone-edu, pandas

import os
import numpy as np
import pandas as pd
import codrone_edu

폴더 = os.path.join(os.path.dirname(codrone_edu.__file__), "data")
모음 = []
for 파일 in sorted(os.listdir(폴더)):
    값 = np.loadtxt(os.path.join(폴더, 파일))
    df = pd.DataFrame(값[:, 1:5], columns=["H", "S", "V", "L"])   # 앞 센서 네 값
    df["순번"] = range(len(df))
    df["색"] = 파일[:-4]                                           # 파일 이름이 곧 정답
    모음.append(df)
색데이터 = pd.concat(모음, ignore_index=True)
색데이터.to_csv("color_data.csv", index=False)

print("전체:", 색데이터.shape)
print(색데이터.groupby("색")[["H", "S", "V", "L"]].mean().round(1))


# ----- 실행 결과 (가상 드론) -----
# 전체: (5600, 6)
#                H     S     V     L
# 색
# black      109.6  42.8  13.5   9.7
# blue       253.4  52.8  45.3  33.3
# green       90.4  71.2  67.3  43.6
# lightblue  163.3  39.4  81.6  65.7
# purple     313.1  58.5  47.7  33.7
# red        139.1  85.9  88.1  49.8
# white       96.0   3.4  99.7  97.9
# yellow      54.1  78.1  93.4  56.5
