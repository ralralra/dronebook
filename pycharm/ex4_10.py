# 예제 4-10. KNN과 결정트리 비교하기
# 4-3 센서 데이터 기반 분류 모델 학습 및 평가
# 필요한 라이브러리: pandas, scikit-learn
# 먼저 ex4_08.py 를 실행해야 합니다. 그 예제가 만든 파일을 이 예제가 읽습니다.

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

색데이터 = pd.read_csv("color_data.csv")
X, y = 색데이터[["H", "S", "V", "L"]], 색데이터["색"]
X학습, X평가, y학습, y평가 = train_test_split(X, y, test_size=0.3, random_state=0, stratify=y)

모델들 = {
    "KNN (이웃 9개, 라이브러리 방식)": KNeighborsClassifier(n_neighbors=9),
    "결정트리 (깊이 4)": DecisionTreeClassifier(max_depth=4, random_state=0),
}
for 이름, 모델 in 모델들.items():
    모델.fit(X학습, y학습)
    print(f"{이름:24s} 정확도 {accuracy_score(y평가, 모델.predict(X평가)) * 100:.1f} %")


# ----- 실행 결과 (가상 드론) -----
# KNN (이웃 9개, 라이브러리 방식)    정확도 96.8 %
# 결정트리 (깊이 4)              정확도 70.3 %
