# 예제 4-13. 앞쪽으로 배우고 뒤쪽으로 시험 보기
# 4-3 센서 데이터 기반 분류 모델 학습 및 평가
# 필요한 라이브러리: pandas, scikit-learn
# 먼저 ex4_08.py 를 실행해야 합니다. 그 예제가 만든 파일을 이 예제가 읽습니다.

import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

색데이터 = pd.read_csv("color_data.csv")
특성 = ["H", "S", "V", "L"]
학습 = 색데이터[색데이터["순번"] < 500]
평가 = 색데이터[색데이터["순번"] >= 500]

knn = KNeighborsClassifier(n_neighbors=9).fit(학습[특성], 학습["색"])
예측 = knn.predict(평가[특성])
print(f"앞 500개로 학습, 뒤 200개로 평가 → 정확도 {accuracy_score(평가['색'], 예측) * 100:.1f} %")
print()
print(pd.crosstab(평가["색"], 예측, rownames=["실제"], colnames=["예측"]))


# ----- 실행 결과 (가상 드론) -----
# 앞 500개로 학습, 뒤 200개로 평가 → 정확도 86.9 %
#
# 예측         black  blue  green  lightblue  purple  red  yellow
# 실제
# black        191     0      9          0       0    0       0
# blue           0   200      0          0       0    0       0
# green          1     0    199          0       0    0       0
# lightblue      0     0      0        200       0    0       0
# purple         0     0      0          0     200    0       0
# red            0     0      0          0       0  200       0
# white          0     0      0        200       0    0       0
# yellow         0     0      0          0       0    0     200
