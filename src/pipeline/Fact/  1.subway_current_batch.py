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
        time.sleep(0.1)
        

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
print(df_subway.glimpse())



import polars as pl

df_clean = df_subway.select([
    # -------------------------------------------------------------------------
    # 1. 🔤 [VARCHAR 타입 존] -> pl.String으로 형변환 (Postgres의 VARCHAR로 매핑)
    # -------------------------------------------------------------------------
    pl.col("USE_MM").cast(pl.String).alias("use_mm"),
    pl.col("SBWY_ROUT_LN_NM").cast(pl.String).alias("sbwy_rout_ln_nm"),
    pl.col("STTN").cast(pl.String).alias("sttn"),
    # -------------------------------------------------------------------------
    # 2. 🔢 [NUMERIC 타입 존] -> pl.Float64로 형변환 (Postgres의 NUMERIC/DOUBLE PRECISION 매핑)
    # (원천 데이터 f64 타입을 유지하되, 혹시 모를 문자열 혼입을 막기 위해 확실하게 캐스팅하네!)
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
    # 💡 자네 로그에서 색출한 00시 ~ 03시 진짜 이름표들!
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
    # (자네 템플릿의 strptime 기믹을 활용해 Postgres의 DATE 규격과 100% 동기화하네!)
    # -------------------------------------------------------------------------
    pl.col("JOB_YMD").str.strptime(pl.Date, format="%Y%m%d").alias("job_ymd")
])

print("✨ [디버깅 & 타입 개조 완료] 원천 스키마가 Postgres 맞춤형(String, Float64, Date)으로 대변신했습니다!")
with pl.Config(tbl_cols=-1):
    print(df_clean.head(5))





# 실무 규격 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

# DB 접속 정보
DB_USER = "krx"
DB_PASSWORD = "krx" 
DB_HOST = "192.168.56.10"
DB_PORT = "5432"
DB_NAME = "bdp_test"
conn_info = f"host={DB_HOST} port={DB_PORT} dbname={DB_NAME} user={DB_USER} password={DB_PASSWORD}"

# 💡 [삭제 후 삽입 스위치] 테스트하고 싶다면 아래 주석을 해제하게나!
# start_date = "202511"
# end_date = "202511"


# ====================================================================
# 1️⃣ [홍 대리 요청] 53개 최종 컬럼 명단 기차 연결 및 콤마 문자열 조립
# ====================================================================
time_cols = []
for i in range(24):
    time_cols.append(f"hr_{i}_get_on_nope")
    time_cols.append(f"hr_{i}_get_off_nope")

# 맨 뒤에 'last_updated' 기차 칸을 명시적으로 결합(Concat)합니다!
final_col_list = ["use_mm", "sbwy_rout_ln_nm", "sttn"] + time_cols + ["job_ymd", "last_updated"]

# 리스트 안의 53개 단어들을 콤마(, )로 엮어서 하나의 긴 문장으로 빌드!
columns_str = ", ".join(final_col_list)


# ====================================================================
# 2️⃣ [홍 대리 요청] Polars 프레임에 실시간 현재 시간 감사 데이터 주입
# ====================================================================
# 원천 API가 주지 않는 'last_updated' 컬럼을 실시간으로 생성하여 병합합니다.
df_final_audit = df_clean.with_columns(
    pl.lit(datetime.now()).alias("last_updated")
).select(final_col_list) # 컬럼 순서를 위 명단과 100% 동치(매핑) 시킵니다.


# ====================================================================
# 3️⃣ 데이터베이스 조건부 삭제 후 초고속 벌크 주입 가동
# ====================================================================
try:
    logging.info("🔗 PostgreSQL 서버에 초고속 벌크 연결을 수립합니다.")
    
    with psycopg.connect(conn_info) as conn:
        with conn.cursor() as cur:
            
            # 날짜 변수(start_date, end_date) 존재 여부 자동 감지 분기
            try:
                v_start = start_date
                v_end = end_date
                
                print(f"🧹 [{v_start} ~ {v_end}] 기간의 기존 데이터를 청소합니다...")
                sql_delete = f"""
                    DELETE FROM ods.TT_seoul_subway_stats_monthly 
                    WHERE use_mm BETWEEN '{v_start}' AND '{v_end}'
                """
                cur.execute(sql_delete)
                logging.info(f"🗑️ [청소 완료] 총 {cur.rowcount}개의 행이 테이블에서 사전 제거되었습니다.")
                
            except NameError:
                # 변수가 없으면 청소 단계 스킵하고 무식하게 대량 적재 모드로 직진!
                logging.info("ℹ️ [스킵] 날짜 변수가 지정되지 않아 기존 데이터 청소 없이 즉시 주입을 시작합니다.")

            # ⚡ Psycopg3 COPY 벌크 엔진 기동
            logging.info(f"📥 감사 컬럼이 포함된 새 데이터 {len(df_final_audit)}건을 테이블에 주입합니다...")
            sql_copy = f"COPY ods.TT_seoul_subway_stats_monthly ({columns_str}) FROM STDIN"
            
            with cur.copy(sql_copy) as copy:
                for row in df_final_audit.iter_rows():
                    copy.write_row(row)
                    
            conn.commit()
            
    logging.info(f"🎉 [작업 성공] 총 {len(df_final_audit)}건의 데이터가 last_updated 타임스탬프와 함께 완전 무결하게 적재되었습니다!")

except Exception as e:
    logging.error(f"❌ 데이터베이스 적재 중 치명적 장애 발생: {e}")



