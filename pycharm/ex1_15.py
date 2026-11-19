# 예제 1-15. 임무를 파일로 저장하고 불러오기
# 1-4 조건·반복·자료구조를 활용한 비행

import json

임무 = [
    {"동작": "전진", "값": 120},
    {"동작": "왼쪽회전", "값": 120},
    {"동작": "전진", "값": 120},
]

with open("mission.json", "w", encoding="utf-8") as f:     # 저장
    json.dump(임무, f, ensure_ascii=False, indent=2)
print("mission.json 으로 저장했습니다.")

with open("mission.json", encoding="utf-8") as f:          # 불러오기
    불러온임무 = json.load(f)

print("불러온 단계 수:", len(불러온임무))
for 단계 in 불러온임무:
    print("  ", 단계)


# ----- 실행 결과 (가상 드론) -----
# mission.json 으로 저장했습니다.
# 불러온 단계 수: 3
#    {'동작': '전진', '값': 120}
#    {'동작': '왼쪽회전', '값': 120}
#    {'동작': '전진', '값': 120}
