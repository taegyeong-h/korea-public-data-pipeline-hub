

# 002_subway_monthly_range.py (기간 반복 실행기)
# 인자값: 두 개 (START_MONTH = "202301", END_MONTH = "202605")

# 역할: 시작월부터 종료월까지의 목록을 만들고, for문을 돌면서 TARGET_MONTH를 바꿔가며 데이터를 누적(Append) 적재합니다.

# 활용도:
# 초기 역사(History) 적재용: 프로젝트 오픈 전 과거 수년 치 데이터를 전월까지 한 번에 싹 밀어 넣을 때 수동으로 실행합니다.


# 002_subway_monthly_history.py (월별 이력 수동 적재)
import polars as pl
from datetime import datetime
import logging

# 1. 수동으로 돌릴 과거 범위를 명시적으로 하드코딩!
START_MONTH = "202301"
END_MONTH = "202605"  # 전월까지 

# 2. Polars의 '1mo(1달)' 간격 기능을 써서 YYYYMM 문자열 리스트를 초고속 생성
# 결과: ['202301', '202302', ..., '202605']
target_months = pl.date_range(
    start=datetime.strptime(START_MONTH, "%Y%m"),
    end=datetime.strptime(END_MONTH, "%Y%m"),
    interval="1mo"
).dt.strftime("%Y%m").to_list()

logging.info(f"⏳ 총 {len(target_months)}개의 월별 이력 데이터를 수동 배치 적재합니다.")

# 3. 월별로 돌면서 우리가 만든 대박 로직(DELETE -> COPY) 실행!
for TARGET_MONTH in target_months:
    logging.info(f"🚀 {TARGET_MONTH} 데이터 백필 시작...")
    
    # 이 안에서 기존 001번의 API 호출, df_clean 생성, cur.copy 엔진이 작동합니다.
    # (매 루프마다 해당 월을 DELETE하고 COPY하므로 중복 걱정이 없습니다.)



# 001_subway_monthly_batch.py (정기 자동 배치)
from datetime import datetime, timedelta
import logging

# 1. 오늘 날짜를 기준으로 '지난달' YYYYMM 문자열을 자동으로 계산
today = datetime.now()
first_day_of_this_month = today.replace(day=1)
last_day_of_last_month = first_day_of_this_month - timedelta(days=1)

# 최종 확정된 자동 타겟팅 월 (예: 오늘이 2026년 6월이면 자동으로 "202605"가 됨)
TARGET_MONTH = last_day_of_last_month.strftime("%Y%m")

logging.info(f"🤖 정기 자동 배치 가동 - 대상 월: {TARGET_MONTH}")

# 2. 이 TARGET_MONTH 하나를 가지고 루프 없이 딱 한 번만 실행!
# 기존에 완성하신 청소(DELETE) 후 초고속 주입(COPY) 로직이 그대로 한 번 실행됩니다.



# 002_subway_monthly_range.py 구조 예시
import polars as pl
from datetime import datetime
import logging

# [인터페이스] 시작월과 종료월 2개를 지정
START_MONTH = "202301"
END_MONTH = "202605"

# Polars로 범위 내의 YYYYMM 리스트 자동 생성
target_months = pl.date_range(
    start=datetime.strptime(START_MONTH, "%Y%m"),
    end=datetime.strptime(END_MONTH, "%Y%m"),
    interval="1mo"
).dt.strftime("%Y%m").to_list()

logging.info(f"⏳ {START_MONTH}부터 {END_MONTH}까지 총 {len(target_months)}개월간 반복 처리를 시작합니다.")

# target_month에 하나씩 할당해가며 loop 작동!
for TARGET_MONTH in target_months:
    logging.info(f"🔄 현재 처리 중인 월: {TARGET_MONTH}")
    
    # 1. 해당 월 기존 데이터 DELETE
    # 2. 해당 월 API 호출 및 정제
    # 3. PostgreSQL COPY 벌크 주입 (기존 테이블에 행이 계속 append(추가)됨)




이번 달: [지하철 이용객수 Fact] + [역 위치 Master] + [호선 정보 Master] ➡️ 지하철 Mart (Airflow DAG 003번)

다음 달: [시내버스 이용객수 Fact] + [정류장 위치 Master] + [버스 노선 Master] ➡️ 버스 Mart (Airflow DAG 004번)
