🚇 서울시 지하철 시간대별 승하차 데이터 EL 파이프라인

# Apache Airflow와 PostgreSQL을 활용하여 서울시 공공데이터 API로부터 2년 치(2025~2026) 지하철 승하차 시계열 데이터를 안정적으로 수집 및 적재(EL)하는 프로젝트입니다.

🛠️ 1. 기술 스택 & 인프라 (Tech Stack)
Language: Python 3.14+
Orchestrator: Apache Airflow 3.2 (LocalExecutor)
Database: PostgreSQL 18 (OLAP 및 Raw Data 저장소)
Environment: Win 10


📅 2. 데이터 소스 명세 (Data Source Specifications)

제공처: 서울열린데이터광장
API 명칭: 서울시 지하철 호선별 역별 시간대별 승하차 인원 정보 (CardSubwayTimeInfo)
데이터 포맷: REST API (JSON)
데이터 갱신 주기: 매월 중순 전월 데이터 최종 확정 및 업데이트
적재 범위: 2024년 01월 ~ 2025년 12월 (총 24개월 데이터, Historical Batch Load)
