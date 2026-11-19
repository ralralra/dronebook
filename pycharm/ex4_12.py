# 예제 4-12. 색상을 고리 위의 점으로 바꾸기
# 4-3 센서 데이터 기반 분류 모델 학습 및 평가
# 필요한 라이브러리: pandas, scikit-learn
# 먼저 ex4_08.py 를 실행해야 합니다. 그 예제가 만든 파일을 이 예제가 읽습니다.

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

색데이터 = pd.read_csv("color_data.csv")
각 = np.radians(색데이터["H"])
색데이터["가로"] = np.cos(각) * 색데이터["S"]
색데이터["세로"] = np.sin(각) * 색데이터["S"]

y = 색데이터["색"]
for 특성 in [["H", "S", "V", "L"], ["가로", "세로", "V", "L"]]:
    X학습, X평가, y학습, y평가 = train_test_split(색데이터[특성], y, test_size=0.3, random_state=0, stratify=y)
    트리 = DecisionTreeClassifier(max_depth=4, random_state=0).fit(X학습, y학습)
    print(f"{str(특성):26s} 결정트리 정확도 {accuracy_score(y평가, 트리.predict(X평가)) * 100:.1f} %")


# ----- 실행 결과 (가상 드론) -----
# ['H', 'S', 'V', 'L']       결정트리 정확도 70.3 %
# ['가로', '세로', 'V', 'L']     결정트리 정확도 85.7 %
