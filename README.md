# 📊 설문조사 입체 분석 대시보드

설문조사 결과를 **정량(객관식) → 정성(주관식) → 연도별 시계열 비교** 3단계로 분석하는 Streamlit 대시보드입니다.
도서관 이용자 만족도 조사를 예시로 만들었지만, 리커트 척도 문항과 주관식 응답이 포함된 일반 설문에도 사용할 수 있습니다.

## 주요 기능

### Stage 1. 객관식 데이터 분석 (정량)
| 단계 | 내용 |
|---|---|
| Step 1 | 데이터 전처리 (결측·무응답 처리, 문항 유형 자동 추론) |
| Step 2 | 인구통계 분석 (성별, 이용자 구분 등) |
| Step 3 | 기술 통계 분석 (평균, 표준편차 등) |
| Step 4 | 문항별 빈도분석 |
| Step 5 | 교차분석 |

### Stage 2. 주관식 데이터 분석 (정성)
| 단계 | 내용 |
|---|---|
| Step 6 | 의미 네트워크 분석 — Kiwi 형태소 분석으로 명사 추출, 동시출현 네트워크 및 커뮤니티 탐지, 두 문항 비교 |
| Step 7 | 공감 맵(Empathy Map) 분석 — Gemini(기본: 3.1 Pro)가 응답을 Says / Thinks / Does / Feels로 정리하고 원문 근거를 검증 |
| Step 8 | HMW(How Might We) 질문 도출 |

### Stage 3. 연도별 시계열 비교 분석
문항 수나 문구가 바뀐 두 연도의 조사를 통계적으로 비교합니다 (`timeseries_analysis.py`).

1. **전반적 만족도 1:1 비교** — 독립표본 t-검정(Levene → Student/Welch), Cohen's d, Mann-Whitney U
2. **상위 차원 통합 비교** — 문항을 3대 차원(자료/정보 · 시설/공간 · 서비스/프로그램)에 매핑, 연도별 Cronbach's α(95% CI), 차원 점수 비교(Welch t, Holm 보정)
3. **영향요인(Driver) 구조 변화** — 연도별 다중회귀(B, β, VIF, R²), Shapley R² 상대중요도, 연도×차원 상호작용 검정

분석 결과는 Excel 파일로 내보낼 수 있습니다.

## 설치 및 실행

Python 3.10 이상을 권장합니다.

```bash
pip install streamlit -r requirements.txt
```

```bash
streamlit run empathy_map.py
```

### Gemini API 키 설정 (Stage 2의 AI 분석 기능)
`.streamlit/secrets.toml` 파일을 만들고 키를 넣으세요. 이 파일은 `.gitignore`에 포함되어 있어 저장소에 올라가지 않습니다.

```toml
GEMINI_API_KEY = "여기에_API_키"
```

secrets 파일이 없으면 앱 사이드바에서 직접 키를 입력할 수 있습니다.

### 단계별 사용 모델

| 단계 | 기능 | 모델 |
|---|---|---|
| Step 6 | 네트워크 분석 (키워드 그룹핑) | Gemini 2.5 Flash (고정) |
| Step 7 | 공감 맵 (통합 · 세그먼트별) | Gemini 3.1 Pro (기본값) / 2.5 Flash 선택 가능 |
| Step 8 | HMW 질문 도출 | Gemini 3.1 Pro (기본값) / 2.5 Flash 선택 가능 |

Step 7·8의 모델은 사이드바의 **"Step 7·8 분석 모델 (공감 맵 · HMW)"** 메뉴에서 바꿀 수 있습니다.

> 💡 **Pro 모델은 새 API 키가 필요 없습니다.** 지금 쓰는 Gemini API 키에 [Google AI Studio](https://aistudio.google.com/)에서 결제(유료 등급)만 연결하면 됩니다.
> Gemini 3.1 Pro(`gemini-3.1-pro-preview`)는 API 무료 등급이 없어 결제 없이 호출하면 429(한도 초과) 오류가 납니다. 결제를 연결하지 않았다면 사이드바에서 **Gemini 2.5 Flash**를 선택하세요.
>
> `gemini-2.5-pro`는 Google 정책상 신규 사용자에게 더 이상 제공되지 않아(404 NOT_FOUND) 3.1 Pro로 교체했습니다.

## 파일 구성

| 파일 | 설명 |
|---|---|
| `empathy_map.py` | 메인 Streamlit 앱 (Stage 1~3 화면) |
| `timeseries_analysis.py` | Stage 3 통계 분석 모듈 (통계 함수는 Streamlit과 독립적) |
| `generate_mock_timeseries_data.py` | Stage 3 테스트용 모의 데이터 생성 스크립트 |
| `mock_survey_2025.csv` | 2025년 모의 설문 데이터 (세부 16문항 + 전반적 만족도) |
| `mock_survey_2026.csv` | 2026년 모의 설문 데이터 (세부 10문항 + 전반적 만족도, 문구 변경) |
| `stage3_timeseries.patch` | Stage 3 기능 추가 시의 변경 내역 (참고용, 이미 반영됨) |
| `requirements.txt` | 의존 패키지 목록 |

## 입력 데이터 형식

- CSV(UTF-8 / CP949 자동 판별) 또는 Excel(`.xlsx`) 파일
- 한 행에 응답자 1명, 한 열에 문항 1개
- 객관식 문항은 리커트 척도 숫자(예: 1~5)로 입력하며, `0`은 '해당없음'으로 보고 결측 처리합니다.

예시 데이터를 다시 만들려면 아래 명령을 실행하세요.

```bash
python generate_mock_timeseries_data.py
```

> 참고: 그래프 PNG 다운로드 시 한글 표시를 위해 `Malgun Gothic` 폰트를 사용합니다 (Windows 기본 폰트).
