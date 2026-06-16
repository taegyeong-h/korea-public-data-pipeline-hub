# 전국 대기오염 측정소 기준 데이터 (Master Data)

## 1. 데이터 출처
- **원본 사이트**: [에어코리아 측정소 정보](https://www.airkorea.or.kr/web/stationInfo?pMENU_NO=93)
- **수집 방법**: 에어코리아 웹사이트 내 '측정소 정보' 메뉴에서 [전체] 조회 후 엑셀 다운로드  

![기준 테이블 경로](https://github.com/user-attachments/assets/fef5a0eb-e1ed-4660-8e7e-e4a3fcacb0fb)

## 2. 데이터 형식 (Sample)
원본 파일의 1~3행(불필요한 헤더 및 빈 행)을 제거하고, 순수 헤더를 4행에서 1행으로 올린 데이터 구조입니다.
![데이터 형식](https://github.com/user-attachments/assets/c20ab0dd-b30a-4dbc-902a-810f5202f9d7)

| 지역명 | 측정소명 | 측정소 주소 | 운영기관 | 설치년도 |
| :--- | :--- | :--- | :--- | :--- |
| 경북 | 3공단 | 경북 포항시 남구 대송면 철강산단로130번길 29 3공단 배수지 | 경상북도보건환경연구원 | 2010 |
| 경기 | 가남읍 | 경기도 여주시 가남읍 태평중앙1길 20 가남읍행정복지센터 옥상 | 경기도보건환경연구원 | 2020 |

## 3. 데이터 전처리 과정 (ETL)
1. **행 제거**: 엑셀에서 1~3행의 타이틀 및 빈 행 삭제.
2. **헤더 고정**: 4행을 컬럼 헤더로 지정.
3. **인코딩 변환**: 파이썬 `Polars` 및 DB 적재 시 오류 방지를 위해 **UTF-8** 형식의 CSV로 저장.
4. **저장 경로**: `./02_nationwide_air_quality/ODS/seed_data/nationwide_air_station.csv`


## 4. 테이블 생성 
  > [!Note]
  >   ODS는 원본 데이터를 그대로 보관하는 곳, 유연한 변경 고속 적재등의 이유로 기본키를 제거 DW(Data Warehouse)에서 잡을 예정
```sql
CREATE TABLE ods.air_station_raw (
    region_nm       VARCHAR(50), 
    station_nm      VARCHAR(100), 
    station_addr    TEXT,
    agency_nm       VARCHAR(100),
    install_year    INTEGER
);
```


## 5. 데이터 가져오기 및 가공
![데이터 가져오기](https://github.com/user-attachments/assets/8b782eb7-4019-4c32-b6c0-95e318f828f5)

```sql
DELETE FROM ods.air_station_raw WHERE region_nm = ''
```
## 6. 기준 테이블 적재 완료
![출력 결과](https://github.com/user-attachments/assets/0945e185-f1c6-42ca-b90c-d16e39b476f9)
