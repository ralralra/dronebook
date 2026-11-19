# 예제 4-7. 결정트리가 찾은 기준과 규칙 비교하기
# 4-2 규칙 기반 제어와 기계학습의 비교
# 필요한 라이브러리: pandas, scikit-learn
# 먼저 ex4_06.py 를 실행해야 합니다. 그 예제가 만든 파일을 이 예제가 읽습니다.

import pandas as pd
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

df = pd.read_csv("flight_decision.csv")
X, y = df[["거리", "기울기", "배터리"]], df["계속"]
X학습, X평가, y학습, y평가 = train_test_split(X, y, test_size=0.3, random_state=20, stratify=y)

모델 = DecisionTreeClassifier(max_depth=3, random_state=20).fit(X학습, y학습)

def 규칙판단(거리, 기울기, 배터리):
    return int(거리 >= 50 and 기울기 <= 8 and 배터리 >= 30)

규칙예측 = [규칙판단(*행) for 행 in X평가.values]
print(f"규칙 정확도: {accuracy_score(y평가, 규칙예측) * 100:.1f} %")
print(f"모델 정확도: {accuracy_score(y평가, 모델.predict(X평가)) * 100:.1f} %")
print()
print(export_text(모델, feature_names=list(X.columns)))


# ----- 실행 결과 (가상 드론) -----
# 규칙 정확도: 95.0 %
# 모델 정확도: 94.2 %
#
# |--- 기울기 <= 7.55
# |   |--- 거리 <= 48.40
# |   |   |--- class: 0
# |   |--- 거리 >  48.40
# |   |   |--- 배터리 <= 29.50
# |   |   |   |--- class: 0
# |   |   |--- 배터리 >  29.50
# |   |   |   |--- class: 1
# |--- 기울기 >  7.55
# |   |--- 기울기 <= 8.95
# |   |   |--- 거리 <= 149.10
# |   |   |   |--- class: 0
# |   |   |--- 거리 >  149.10
# |   |   |   |--- class: 1
# |   |--- 기울기 >  8.95
# |   |   |--- class: 0
