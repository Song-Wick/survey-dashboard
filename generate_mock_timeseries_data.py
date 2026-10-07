"""
Stage 3(연도별 시계열 비교) 테스트용 모의 데이터 생성
 - 2025년: 세부 16문항 + '17. 전반적 이용 만족도' (총 17문항)
 - 2026년: 세부 10문항 + '전반적 만족도'         (총 11문항, 문구 변경)
잠재 차원(자료/정보, 시설/공간, 서비스/프로그램)에서 문항 응답을 생성하여
신뢰도·회귀 결과가 현실적으로 나오도록 구성. 2026년은 핵심 동인이 '시설/공간'으로 이동하도록 설정.
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(2026)


def likert(latent, noise=0.7, shift=0.0):
    raw = 3.4 + shift + latent + rng.normal(0, noise, len(latent))
    return np.clip(np.rint(raw), 1, 5).astype(int)


def make_year(n, items, weights, dim_shift, overall_name):
    z = rng.multivariate_normal([0, 0, 0], [[1, .45, .4], [.45, 1, .4], [.4, .4, 1]], n) * 0.8
    df = pd.DataFrame({
        "성별": rng.choice(["남성", "여성"], n),
        "이용자 구분": rng.choice(["학부생", "대학원생", "교직원"], n, p=[.6, .3, .1]),
    })
    for name, dim in items:
        df[name] = likert(z[:, dim], shift=dim_shift[dim])
    overall = 3.5 + z @ np.array(weights) + rng.normal(0, 0.55, n)
    df[overall_name] = np.clip(np.rint(overall), 1, 5).astype(int)
    # 일부 '해당없음(0)' 응답 → 분석 시 결측 처리 확인용
    df.iloc[rng.choice(n, 5, replace=False), 3] = 0
    return df


items_2025 = [
    ("1. 소장 자료(도서)의 충분성", 0), ("2. 전자자료(DB·전자저널) 이용 편의", 0),
    ("3. 자료 검색 시스템 만족도", 0), ("4. 희망도서 신청 및 구입 처리", 0), ("5. 학술 정보 제공의 신속성", 0),
    ("6. 열람실 좌석 이용 환경", 1), ("7. 시설 청결 상태", 1), ("8. 냉난방·조명 등 쾌적성", 1),
    ("9. PC·와이파이 등 장비 환경", 1), ("10. 스터디룸 등 공간 이용", 1),
    ("11. 직원 친절도", 2), ("12. 대출·반납 서비스", 2), ("13. 이용자 교육 프로그램", 2),
    ("14. 홈페이지 안내 서비스", 2), ("15. 문화 행사 프로그램", 2), ("16. 참고 상담 서비스", 2),
]
items_2026 = [
    ("자료 보유 및 접근성", 0), ("전자정보 검색 편의성", 0), ("신착 자료 제공", 0),
    ("공간 쾌적성", 1), ("좌석 및 시설 이용", 1), ("장비·기기 환경", 1),
    ("직원 응대 친절", 2), ("대출·반납 등 서비스 편의", 2), ("교육 및 문화 프로그램", 2), ("홈페이지 정보 안내", 2),
]

df25 = make_year(220, items_2025, weights=[.45, .2, .3], dim_shift=[0, -.2, .1], overall_name="17. 전반적 이용 만족도")
df26 = make_year(240, items_2026, weights=[.25, .5, .2], dim_shift=[.05, .2, .1], overall_name="전반적 만족도")

df25.to_csv("mock_survey_2025.csv", index=False, encoding="utf-8-sig")
df26.to_csv("mock_survey_2026.csv", index=False, encoding="utf-8-sig")
print("mock_survey_2025.csv / mock_survey_2026.csv 생성 완료")
