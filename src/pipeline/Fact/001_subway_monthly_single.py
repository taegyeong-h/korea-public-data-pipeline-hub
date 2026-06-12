"""
서울시 지하철 이용객 데이터 수집 배치 스크립트

- 기능: 년월 데이터(YYYYMM) 하나의 인자값을 받아 서울 열린데이터 광장 API로부터 데이터를 가져옵니다.
- DB 연동: 수집 및 정제된 데이터는 [sql/ods/get_TT_seoul_subway_monthly] 테이블과 연결되어 COPY 명령어를 이용하여 데이터를 적재합니다 
- 작성일: 2026년 6월 11일
- 작성자: 홍태경
"""

pip install polars requests sqlalchemy psycopg2-binary psycopg psycopg-binary 

import requests
import polars as pl
import psycopg
import time
from datetime import datetime
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# 1. 필수 인자 (정식 명세서의 필수 항목들)
API_KEY = "7656714c4567757336356769446c6b"      # KEY: 고유 인증키
REQ_TYPE = "json"                             # TYPE: json 파일 형식
SERVICE_NAME = "CardSubwayTime"               # SERVICE: 시간대별 지하철역 승객 현황 조회 식별자
START_INDEX = 1                               # START_INDEX: 페이징 시작 행 번호
END_INDEX = 5                                 # END_INDEX: 페이징 종료 행 번호 (우선 맛보기로 5행만!)
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

        logging.info(res_rows)
    else:
        logging.error(f"API 요청에 실패했습니다. 상태 코드: {response.status_code}")
except Exception as e:
    logging.error(f" 파이프라인 통신 중 치명적 에러 발생: {e}")

df_subway = pl.DataFrame(res_rows)
print(df_subway)

target_duplicates = df_subway.filter(
    pl.struct(["USE_MM", "SBWY_ROUT_LN_NM", "STTN"]).is_duplicated()
)
print(target_duplicates)
print(df_subway.glimpse())

df_clean = df_subway.select([
    # -------------------------------------------------------------------------
    # 1. 🔤 [VARCHAR 타입 존] -> pl.String으로 형변환 (Postgres의 VARCHAR로 매핑)
    # -------------------------------------------------------------------------
    pl.col("USE_MM").cast(pl.String).alias("use_mm"),
    pl.col("SBWY_ROUT_LN_NM").cast(pl.String).alias("sbwy_rout_ln_nm"),
    pl.col("STTN").cast(pl.String).alias("sttn"),
    # -------------------------------------------------------------------------
    # 2. 🔢 [NUMERIC 타입 존] -> pl.Float64로 형변환 (Postgres의 NUMERIC/DOUBLE PRECISION 매핑)
    # -------------------------------------------------------------------------
    pl.col("HR_4_GET_ON_NOPE").cast(pl.Float64).alias("hr_4_get_on_nope"),
    pl.col("HR_4_GET_OFF_NOPE").cast(pl.Float64).alias("hr_4_get_off_nope"),
    pl.col("HR_5_GET_ON_NOPE").cast(pl.Float64).alias("hr_5_get_on_nope"),
    pl.col("HR_5_GET_OFF_NOPE").cast(pl.Float64).alias("hr_5_get_off_nope"),
    pl.col("HR_6_GET_ON_NOPE").cast(pl.Float64).alias("hr_6_get_on_nope"),
    pl.col("HR_6_GET_OFF_NOPE").cast(pl.Float64).alias("hr_6_get_off_nope"),
    pl.col("HR_7_GET_ON_NOPE").cast(pl.Float64).alias("hr_7_get_on_nope"),
    pl.col("HR_7_GET_OFF_NOPE").cast(pl.Float64).alias("hr_7_get_off_nope"),
    pl.col("HR_8_GET_ON_NOPE").cast(pl.Float64).alias("hr_8_get_on_nope"),
    pl.col("HR_8_GET_OFF_NOPE").cast(pl.Float64).alias("hr_8_get_off_nope"),
    pl.col("HR_9_GET_ON_NOPE").cast(pl.Float64).alias("hr_9_get_on_nope"),
    pl.col("HR_9_GET_OFF_NOPE").cast(pl.Float64).alias("hr_9_get_off_nope"),
    pl.col("HR_10_GET_ON_NOPE").cast(pl.Float64).alias("hr_10_get_on_nope"),
    pl.col("HR_10_GET_OFF_NOPE").cast(pl.Float64).alias("hr_10_get_off_nope"),
    pl.col("HR_11_GET_ON_NOPE").cast(pl.Float64).alias("hr_11_get_on_nope"),
    pl.col("HR_11_GET_OFF_NOPE").cast(pl.Float64).alias("hr_11_get_off_nope"),
    pl.col("HR_12_GET_ON_NOPE").cast(pl.Float64).alias("hr_12_get_on_nope"),
    pl.col("HR_12_GET_OFF_NOPE").cast(pl.Float64).alias("hr_12_get_off_nope"),
    pl.col("HR_13_GET_ON_NOPE").cast(pl.Float64).alias("hr_13_get_on_nope"),
    pl.col("HR_13_GET_OFF_NOPE").cast(pl.Float64).alias("hr_13_get_off_nope"),
    pl.col("HR_14_GET_ON_NOPE").cast(pl.Float64).alias("hr_14_get_on_nope"),
    pl.col("HR_14_GET_OFF_NOPE").cast(pl.Float64).alias("hr_14_get_off_nope"),
    pl.col("HR_15_GET_ON_NOPE").cast(pl.Float64).alias("hr_15_get_on_nope"),
    pl.col("HR_15_GET_OFF_NOPE").cast(pl.Float64).alias("hr_15_get_off_nope"),
    pl.col("HR_16_GET_ON_NOPE").cast(pl.Float64).alias("hr_16_get_on_nope"),
    pl.col("HR_16_GET_OFF_NOPE").cast(pl.Float64).alias("hr_16_get_off_nope"),
    pl.col("HR_17_GET_ON_NOPE").cast(pl.Float64).alias("hr_17_get_on_nope"),
    pl.col("HR_17_GET_OFF_NOPE").cast(pl.Float64).alias("hr_17_get_off_nope"),
    pl.col("HR_18_GET_ON_NOPE").cast(pl.Float64).alias("hr_18_get_on_nope"),
    pl.col("HR_18_GET_OFF_NOPE").cast(pl.Float64).alias("hr_18_get_off_nope"),
    pl.col("HR_19_GET_ON_NOPE").cast(pl.Float64).alias("hr_19_get_on_nope"),
    pl.col("HR_19_GET_OFF_NOPE").cast(pl.Float64).alias("hr_19_get_off_nope"),
    pl.col("HR_20_GET_ON_NOPE").cast(pl.Float64).alias("hr_20_get_on_nope"),
    pl.col("HR_20_GET_OFF_NOPE").cast(pl.Float64).alias("hr_20_get_off_nope"),
    pl.col("HR_21_GET_ON_NOPE").cast(pl.Float64).alias("hr_21_get_on_nope"),
    pl.col("HR_21_GET_OFF_NOPE").cast(pl.Float64).alias("hr_21_get_off_nope"),
    pl.col("HR_22_GET_ON_NOPE").cast(pl.Float64).alias("hr_22_get_on_nope"),
    pl.col("HR_22_GET_OFF_NOPE").cast(pl.Float64).alias("hr_22_get_off_nope"),
    pl.col("HR_23_GET_ON_NOPE").cast(pl.Float64).alias("hr_23_get_on_nope"),
    pl.col("HR_23_GET_OFF_NOPE").cast(pl.Float64).alias("hr_23_get_off_nope"), 
    pl.col("HR_0_GET_ON_NOPE").cast(pl.Float64).alias("hr_0_get_on_nope"),
    pl.col("HR_0_GET_OFF_NOPE").cast(pl.Float64).alias("hr_0_get_off_nope"),
    pl.col("HR_1_GET_ON_NOPE").cast(pl.Float64).alias("hr_1_get_on_nope"),
    pl.col("HR_1_GET_OFF_NOPE").cast(pl.Float64).alias("hr_1_get_off_nope"),
    pl.col("HR_2_GET_ON_NOPE").cast(pl.Float64).alias("hr_2_get_on_nope"),
    pl.col("HR_2_GET_OFF_NOPE").cast(pl.Float64).alias("hr_2_get_off_nope"),
    pl.col("HR_3_GET_ON_NOPE").cast(pl.Float64).alias("hr_3_get_on_nope"),
    pl.col("HR_3_GET_OFF_NOPE").cast(pl.Float64).alias("hr_3_get_off_nope"),
    
    # -------------------------------------------------------------------------
    # 3. 📅 [DATE 타입 존] -> '20251203' 글자를 진짜 날짜 객체로 변환!
    # -------------------------------------------------------------------------
    pl.col("JOB_YMD").str.strptime(pl.Date, format="%Y%m%d").alias("job_ymd")
])

# Postgres DB 접속 정보
DB_USER = "krx"
DB_PASSWORD = "krx" 
DB_HOST = "192.168.56.10"
DB_PORT = "5432"
DB_NAME = "bdp_test"
conn_info = f"host={DB_HOST} port={DB_PORT} dbname={DB_NAME} user={DB_USER} password={DB_PASSWORD}"

time_cols = []
for i in range(24):
    time_cols.append(f"hr_{i}_get_on_nope")
    time_cols.append(f"hr_{i}_get_off_nope")

# 맨 뒤에 'last_updated' 기차 칸을 명시적으로 결합(Concat)합니다!
final_col_list = ["use_mm", "sbwy_rout_ln_nm", "sttn"] + time_cols + ["job_ymd", "last_updated"]

"""
[
    "use_mm", "sbwy_rout_ln_nm", "sttn",           # 앞부분 (3개)
    "hr_0_get_on_nope", "hr_0_get_off_nope",       # 0시 승하차
    "hr_1_get_on_nope", "hr_1_get_off_nope",       # 1시 승하차
    "hr_2_get_on_nope", "hr_2_get_off_nope",       # 2시 승하차
    # ... (중간 생략) ...
    "hr_22_get_on_nope", "hr_22_get_off_nope",     # 22시 승하차
    "hr_23_get_on_nope", "hr_23_get_off_nope",     # 23시 승하차
    "job_ymd", "last_updated"                      # 뒷부분 (2개)
]
"""

# 리스트 안의 53개 단어들을 콤마(, )로 엮어서 하나의 긴 문장으로 빌드!
columns_str = ", ".join(final_col_list)

# "use_mm, sbwy_rout_ln_nm, sttn, hr_0_get_on_nope, hr_0_get_off_nope, hr_1_get_on_nope, hr_1_get_off_nope, hr_2_get_on_nope, hr_2_get_off_nope, ... (중간 생략) ..., hr_22_get_on_nope, hr_22_get_off_nope, hr_23_get_on_nope, hr_23_get_off_nope, job_ymd, last_updated"

# 원천 API가 주지 않는 'last_updated' 컬럼을 실시간으로 생성하여 병합합니다.
df_final_audit = df_clean.with_columns(
    pl.lit(datetime.now()).alias("last_updated")
).select(final_col_list) # 컬럼 순서를 위 명단과 100% 동치(매핑) 시킵니다.


# ====================================================================
# 3️⃣ 데이터베이스 조건부 삭제 후 초고속 벌크 주입 가동
# ====================================================================
try:
    logging.info("🔗 PostgreSQL 서버에 초고속 벌크 연결을 수립합니다.")
    
    # 1. DB 연결 (with절을 나가면 자동 커밋 & 자동 닫기)
    with psycopg.connect(conn_info) as conn:
        # 2. 일꾼(커서) 생성
        with conn.cursor() as cur:
                
            # 💡 [교정] try-except 대신 변수가 진짜 존재하는지 안전하게 검사!
            if 'TARGET_MONTH' in locals() and TARGET_MONTH:
                logging.info(f"[청소 단계] 기존에 존재하는 {TARGET_MONTH}년월 데이터를 청소합니다.")
                cur.execute(
                    "DELETE FROM ods.TT_seoul_subway_stats_monthly WHERE use_mm = %s", 
                    (TARGET_MONTH,)
                )
            else:
                # 위에서 TARGET_MONTH가 선언되지 않았다면 안전하게 이쪽으로 빠집니다.
                logging.info("ℹ️ [스킵] 날짜 변수가 지정되지 않아 기존 데이터 청소 없이 즉시 주입을 시작합니다.")

            # 현재 데이터가 Postgres 서버 하드디스크가 아닌 Polars 데이터프레임에 있으니
            # FROM STDIN은 "네 컴퓨터에 있는 파일 읽지 말고, 지금부터 나(파이썬)가 네트워크 파이프라인을 통해 입으로 직접 쏴주는 데이터 스트림을 그대로 받아먹어라!" 라고 지시하는 것입니다.
            
            # Psycopg3 COPY 벌크 엔진 기동
            logging.info(f"감사 컬럼이 포함된 새 데이터 {len(df_final_audit)}건을 테이블에 주입합니다...")
            sql_copy = f"COPY ods.TT_seoul_subway_stats_monthly ({columns_str}) FROM STDIN"  
            
            with cur.copy(sql_copy) as copy:               # 1. 파이썬과 DB 사이에 고속 빨대(통로)를 꽂습니다.
                for row in df_final_audit.iter_rows():     # 2. Polars에서 데이터를 한 줄(Row)씩 꺼냅니다.
                    copy.write_row(row)                    # 3. 꺼낸 데이터를 그 빨대(STDIN 통로) 속으로 슉슉 던집니다.
    logging.info(f"🎉 [작업 성공] 총 {len(df_final_audit)}건의 데이터가 완전 무결하게 적재되었습니다!")

except Exception as e:
    # DB 연결 실패, COPY 에러 등 모든 예외는 이 대왕 except가 싹 잡아내어 안전하게 처리합니다.
    logging.error(f"❌ 데이터베이스 적재 중 치명적 장애 발생: {e}")



