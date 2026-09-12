# 인플레이션 나침반 · 로컬 앱

기존 stock_info의 카드형 메뉴, 조건 입력 → 결과 화면, 색상과 버튼 형태를 참고한 **별도 Streamlit 앱**입니다. 기존 프로젝트는 수정하지 않았습니다.

## 실행

이 폴더의 PowerShell에서 `./start.ps1`을 실행한 뒤 http://localhost:8511 을 엽니다.
현재 `.venv`가 준비되어 있습니다. 다른 PC에서는 Python 3.12 이상으로 가상환경을 만든 후 `pip install -r requirements.txt`를 실행하세요.

## Streamlit Community Cloud 배포

이 폴더를 GitHub 저장소 루트로 올리고 Streamlit Community Cloud에서 메인 파일을 `app.py`로 지정합니다. 앱 실행에 필요한 `data/prices.csv`, `data/T5YIE.csv`, `data/manifest.json`, `results/summary.csv`, `results/report.html`도 저장소에 포함해야 합니다. `.venv`와 원본 JSON은 `.gitignore`로 제외됩니다.

배포된 앱은 저장소에 포함된 데이터로 바로 실행되므로 별도 API 키가 필요 없습니다. 데이터는 자동 갱신되지 않습니다. 새 데이터가 필요할 때 로컬에서 `python download_data.py`와 `python run_research.py`를 차례로 실행하고 변경된 CSV·보고서를 다시 커밋하세요.

## 기능

- 모델 설명과 국면별 ETF 배분
- 기간, 금액, 임계값, 이동평균, 거래 지연, 비용을 바꾸는 백테스트
- SPY 대비 자산 가치, 일별/월별 낙폭, 거래 내역, CSV 묶음 다운로드
- SPY와 200일 평균, T5YIE 수준·60일 변화, 업종 바스켓 지표·60일 회귀 기울기의 수치와 그래프
- 네 조건의 월말 충족 여부, 결합된 인플레이션 ON/OFF, 다음 달 보유 자산 기록
- 재현 가정, 보수적 가정, 신호 제거 실험과 파라미터 민감도 보고서

`python download_data.py`는 Yahoo Finance ETF 조정 가격과 FRED 데이터를 수집합니다. 최초 수집 종료일은 2026-09-09로 고정되어 있습니다. 이후 갱신하려면 download_data.py의 end를 변경하세요. 저장된 원본만으로 `python run_research.py`를 재실행할 수 있습니다. `python -m unittest test_compass.py`는 미래 데이터 누출, 신호 지연, 혼합 보유 비중 변화와 비용 처리를 검사합니다.

## 검증 범위와 한계

2003년 이전 가격은 이동평균과 업종 바스켓 지표의 준비에 사용합니다. IEF는 상장 전 가격이 없지만 실제 투자 시작 전이므로 신호 계산에는 영향을 주지 않습니다. 모든 신호 입력의 준비 기간이 끝난 첫 월말부터 투자하므로 결과의 실제 시작일을 반드시 보세요. ETF는 Yahoo 조정 종가, 원문은 AllocateSmartly 업종 자료를 사용하므로 완벽한 일치가 보장되지 않습니다. FRED 과거 공개본은 확보하지 않았습니다. 월말 당일 신호·체결은 이상적인 재현 가정이며 별도로 다음 거래일 종가 체결을 비교합니다.

성과는 USD, 샤프의 무위험수익률은 0%, XLP/IEF는 월별 50:50 조정입니다. CPI 자료는 수집했지만 CPI 구간 분석은 아직 구현하지 않았습니다. 파라미터 민감도는 표본 외 검증이 아닙니다. 결과 보고서와 매월 거래 내역은 results/에 있습니다.

출처: [CSS Analytics 모델 원문](https://cssanalytics.wordpress.com/2026/07/27/the-inflation-compass-model/), [FRED T5YIE](https://fred.stlouisfed.org/series/T5YIE), [연준 PCE 물가 목표](https://www.federalreserve.gov/faqs/economy_14400.htm).
