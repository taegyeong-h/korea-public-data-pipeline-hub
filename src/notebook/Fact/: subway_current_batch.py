%pip install polars requests pandas sqlalchemy psycopg2-binary psycopg psycopg-binary 

import requests
import polars as pl
import psycopg
import time
from datetime import datetime
import logging

# 1. 2026년  실무 규격 로깅(Logging) 세팅
# 로그 출력 형태: [시간] [로그레벨] 메시지 형태로 콘솔에 찍히도록 설정합니다.

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# 1. 필수 인자 (정식 명세서의 필수 항목들)
API_KEY = "7656714c4567757336356769446c6b"      # KEY: 고유 인증키
REQ_TYPE = "json"                             # TYPE: xml 대신 json 파일 형식
SERVICE_NAME = "CardSubwayTime"               # SERVICE: 시간대별 지하철역 승객 현황 조회 식별자
START_INDEX = 1                               # START_INDEX: 페이징 시작 행 번호
END_INDEX = 5                                 # END_INDEX: 페이징 종료 행 번호 (우선 맛보기로 5줄만!)
TARGET_MONTH = "202511"                       # USE_MM: 조회하고자 하는 사용월 (YYYYMM)
ROUTE_LINE = ""                               # SBWY_ROUT_LN_NM: 호선명 (예: "1호선")
STATION_NAME = ""                             # STTN: 지하철역명 (예: "서울역")

# 1. 명세서에 명시된 슬래시(/) 가이드라인에 맞추어 주소를 칸칸이 조립합니다.
# 규칙: 기본주소/인증키/파일형식/서비스명/시작번호/종료번호/사용월
base_url = f"http://openapi.seoul.go.kr:8088/{API_KEY}/{REQ_TYPE}/{SERVICE_NAME}/{START_INDEX}/{END_INDEX}/{TARGET_MONTH}"

if ROUTE_LINE != "":
    base_url += f"/{ROUTE_LINE}"
    if STATION_NAME != "":
        base_url += f"/{STATION_NAME}"

logging.info(f"원천 서버 통신 시도 중... (URL: {base_url})")

try:
    response = requests.get(base_url, timeout=10)   ## 서버가 응답할 때까지 무한대로 기다리게 하는 것은 위험하므로, 타임아웃을 10초로 설정합니다.

    if response.status_code == 200:
        logging.info("원천 서버로부터 200 OK 응답 수신 성공!")

        res_json = response.json()
        total = res_json.get("CardSubwayTime")
        res_rows = total.get("row")
        

        logging.info("응답 데이터 (JSON):")
        logging.info(res_rows)
    else:
        logging.error(f"API 요청에 실패했습니다. 상태 코드: {response.status_code}")
except Exception as e:
    logging.error(f"💥 파이프라인 통신 중 치명적 에러 발생: {e}")


df_subway = pl.DataFrame(res_rows)
print(df_subway)

df_staging = df_subway.unique()
print(df_staging)


target_duplicates = df_subway.filter(
    pl.struct(["USE_MM", "SBWY_ROUT_LN_NM", "STTN"]).is_duplicated()
)
print(target_duplicates)



