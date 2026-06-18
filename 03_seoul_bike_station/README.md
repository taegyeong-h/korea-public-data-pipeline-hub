# 🚲 서울시 공공자전거(따릉이) 이용 현황 ELT 파이프라인

본 파이프라인은 서울열린데이터광장의 데이터를 활용하여, **[서울시 자치구별 공공자전거 대여소 가용성 및 이용 패턴 분석 마트]**를 구축하기 위한 데이터 정의 및 정보계 모델링 스터디를 기록합니다.

## 1. 기회 의도 및 데이터 선정 사유
서울시 전역의 자전거 대여소 데이터를 다각도로 분석하여, **"어느 자치구의 대여소가 가장 붐비는가?"** 라는 비즈니스 가설을 검증하고자 합니다.

## 2. 데이터 모델링 전략 (Star Schema)
> 데이터의 성격에 맞춰 **기준 데이터(Dimension)**와 **실적 데이터(Fact)**를 이원화하여 관리합니다.  
> [Fact] API -> 년,월,일 Parquet 포멧 나눠 데이터레이크 저장 (로컬 SSD OR 클라우드 스토리지) -> Temp_ODS(Postgres) -> ODS(Postgres) -> DW(Postgres) -> DM(Postgres) 

> [DIM]  API -> 데이터레이크 (로컬 SSD OR 클라우드 스토리지) -> Temp_ODS(Postgres) -> ODS(Postgres) -> DW(Postgres) -> DM(Postgres)

### A. 기준 데이터 (Dimension Table)
* **대상**: [서울시 공공자전거 대여소 정보](https://data.seoul.go.kr/dataList/OA-15493/A/1/datasetView.do)
* **역할**: 대여소 번호에 따른 자치구, 위치 정보(위도/경도) 매핑
* **원천 데이터 수**: 3000개 미만  

### B. 실적 데이터 (Fact Table)
* **대상**: 2025년 서울특별시 공공자전거 일별 대여정보
* **역할**: 대여소별 일별 '현재 대여 가능한 자전거 수' 추적
* **원천 데이터 수**: 일별 평균 5만개, 월 평균 130만개 

## 3. 수집 대상 데이터셋 명세
| 데이터 분류 | 데이터명 | 파일/스크립트명 | 주기 | 포맷 |
| :--- | :--- | :--- | :--- | :--- |
| **Dimension** | 서울시 공공자전거 대여소 현황 | `extract_dim_seoul_bike_station.csv` | 월별  | API(JSON) |
| **Fact** | 공공자전거 일별 대여정보 | `extract_fact_bike_daily.py`      | 매일 새벽 | API(JSON) |
