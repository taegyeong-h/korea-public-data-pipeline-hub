



-- CREATE TABLE dm.tt_subway_elevator_load_monthly (
--       use_mm                  VARCHAR(6)   NOT NULL  -- 년월 (ex: 202512)
--     , sttn                    VARCHAR(100) NOT NULL  -- 역 이름 (ex: 시청)
--     , rush_hour_riders        BIGINT       NOT NULL  -- 해당 역의 모든 노선 합산 총 출근객 수
--     , elevator_count          INTEGER      NOT NULL  -- 해당 역에 설치된 총 엘리베이터 대수
--     , riders_per_elevator     VARCHAR(50)  NOT NULL  -- 엘리베이터 1대당 부담 인원 
--     , monthly_congestion_rank INTEGER      NOT NULL  -- 대당 부담 인원 기준 월별 순위
--     , last_update             TIMESTAMP    DEFAULT CURRENT_TIMESTAMP -- 💥 데이터 적재/변경 시간
--     , CONSTRAINT pk_subway_elevator_load_monthly PRIMARY KEY (use_mm, sttn)
-- );





INSERT INTO dm.tt_subway_elevator_load_monthly (
    use_mm, sttn, rush_hour_riders, elevator_count, riders_per_elevator, monthly_congestion_rank
)
WITH fact_monthly_summary AS (
    -- ① dw의 팩트 테이블에서 환승역 노선별 데이터를 역 이름 기준으로 미리 SUM 합산!
    SELECT 
          use_mm
        , sttn
        , SUM(hr_8_get_on_nope) AS total_riders
    FROM dw.tt_seoul_subway_stats_monthly
    GROUP BY use_mm, sttn
),

elevator_master_summary AS (
    -- ② dw의 엘리베이터 마스터에서 역별 총 대수를 미리 COUNT 요약!
    SELECT 
          subway_station_name
        , COUNT(node_id) AS total_elevators
    FROM dw.tm_seoul_subway_elevator_master
    WHERE deleted_yn != 'Y'
    GROUP BY subway_station_name
),

mart_base_calculations AS (
    -- ③ 요약된 두 방을 조인하여 부하 지수 계산 및 DENSE_RANK 랭킹 산출 완료!
    SELECT 
          f.use_mm
        , f.sttn
        , f.total_riders AS rush_hour_riders
        , COALESCE(e.total_elevators, 0) AS elevator_count
        , CASE 
            WHEN COALESCE(e.total_elevators, 0) = 0 THEN '인프라 전무(위험)'
            ELSE TO_CHAR(f.total_riders / NULLIF(e.total_elevators, 0), '999,999') || ' 명'
          END AS riders_per_elevator
        , DENSE_RANK() OVER (
            PARTITION BY f.use_mm 
            ORDER BY (f.total_riders / NULLIF(e.total_elevators, 0)) DESC NULLS FIRST
          ) AS monthly_congestion_rank
    FROM fact_monthly_summary f
    LEFT JOIN elevator_master_summary e 
      ON f.sttn = e.subway_station_name
)
-- 🏁 4단계: WITH 절이 다 차려놓은 3번 방 결과물을 마트 테이블에 그대로 부어버리기!
SELECT 
      use_mm
    , sttn
    , rush_hour_riders
    , elevator_count
    , riders_per_elevator
    , monthly_congestion_rank
FROM mart_base_calculations

-- 💥 [안전 장치] 혹시나 동일한 년월+역이름 데이터가 또 들어오면 덮어쓰고 last_update 갱신!
ON CONFLICT (use_mm, sttn) DO UPDATE 
SET rush_hour_riders        = EXCLUDED.rush_hour_riders,
    elevator_count          = EXCLUDED.elevator_count,
    riders_per_elevator     = EXCLUDED.riders_per_elevator,
    monthly_congestion_rank = EXCLUDED.monthly_congestion_rank,
    last_update             = CURRENT_TIMESTAMP; -- 변경된 현재 시간으로 동적 리프레시!
