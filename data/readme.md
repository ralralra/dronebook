# data

교재 'AI 드론 데이터 코딩'과 'AI 드론 지능형 제어'의 예제가 쓰는 파일입니다.
코랩 노트의 준비 셀과 '실제 데이터로 해 보기'의 코드가 이 폴더에서 파일을 바로 읽습니다.

| 파일 | 내용 | 출처와 이용 조건 |
| :-- | :-- | :-- |
| `drone_sim.py` | 수업용 가상 드론 모듈 | 이 교재를 위해 만든 파일 |
| `font_setup.py` | 그래프의 한글 글꼴 설정 | 이 교재를 위해 만든 파일 |
| `kios_flights.csv` | 산업용 드론(DJI Matrice 300)의 실제 비행 기록 7회, 0.1초 간격, 54,726줄 | Palamas, A. & Kolios, P. (2023). *Drone onboard multi-modal sensor dataset*. KIOS Research and Innovation Center of Excellence, University of Cyprus. Zenodo. doi:10.5281/zenodo.7643456. CC BY 4.0 |
| `drone_minwon.xlsx` | 드론 원스톱 민원 신청 건수(2020년 8월~2025년 6월, 월별) | 국토교통부 서울지방항공청, 공공데이터포털. 이용허락범위 제한 없음 |

## 원본에서 바꾼 것

`kios_flights.csv`는 원본을 수업에 맞게 줄인 파일입니다.

- 원본의 32개 열 가운데 `flight`, `seq`, `wind_speed`, `battery_voltage`, `battery_current`, `position_z` 여섯 열만 남겼습니다.
- `wind_speed`와 `position_z`를 소수 둘째 자리로 반올림했습니다.
- 줄 수와 줄의 순서, 구분자(`;`)는 원본 그대로입니다.

`drone_minwon.xlsx`는 내려받은 파일 그대로입니다.
