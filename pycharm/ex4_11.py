# 예제 4-11. 혼동 행렬로 틀린 곳 찾기
# 4-3 센서 데이터 기반 분류 모델 학습 및 평가
# 필요한 라이브러리: pandas, scikit-learn
# 먼저 ex4_08.py 를 실행해야 합니다. 그 예제가 만든 파일을 이 예제가 읽습니다.

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

색데이터 = pd.read_csv("color_data.csv")
X, y = 색데이터[["H", "S", "V", "L"]], 색데이터["색"]
X학습, X평가, y학습, y평가 = train_test_split(X, y, test_size=0.3, random_state=0, stratify=y)
트리 = DecisionTreeClassifier(max_depth=4, random_state=0).fit(X학습, y학습)

표 = pd.crosstab(y평가, 트리.predict(X평가), rownames=["실제"], colnames=["예측"])
print(표)


# ----- 실행 결과 (가상 드론) -----
# 예측         black  blue  lightblue  purple  white  yellow
# 실제
# black        187     0          0       0      0      23
# blue           0   182          0      28      0       0
# green          0     0          0       0      0     210
# lightblue      0     0        182       0     28       0
# purple         0     0          0     210      0       0
# red            0     0          0      71      0     139
# white          0     0          0       0    210       0
# yellow         0     0          0       0      0     210
