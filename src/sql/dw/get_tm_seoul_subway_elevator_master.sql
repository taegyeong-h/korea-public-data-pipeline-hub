CREATE TABLE dw.get_tm_seoul_subway_elevator_master (
    node_id                      VARCHAR(50) PRIMARY KEY, -- 엘리베이터 고유 코드
    -- ② 원천 컬럼 풀네임 매핑 10개 (가독성 100%)
    node_link_type               VARCHAR(50),             -- 노드링크 유형
    node_wkt                     TEXT,                    -- 공간 좌표 문자열
    node_type_code               VARCHAR(10),             -- 노드 유형 코드
    sigungu_code                 VARCHAR(20),             -- 시군구코드
    sigungu_name                 VARCHAR(100),            -- 시군구명
    eupmyeondong_code            VARCHAR(20),             -- 읍면동코드
    eupmyeondong_name            VARCHAR(100),            -- 읍면동명
    subway_station_code          VARCHAR(20),             -- 지하철역코드 (무적의 안전 조인 키!)
    subway_station_name          VARCHAR(100),            -- 지하철역명
    created_at                   TIMESTAMP NOT NULL DEFAULT NOW(), -- 최초 적재 시각
    last_updated                 TIMESTAMP NOT NULL DEFAULT NOW(), -- 최종 수정 시각 (Current Datetime 자동 주입)
    deleted_yn                   CHAR(1) NOT NULL DEFAULT 'N'      -- 삭제 여부 플래그 ('Y' 또는 'N'만 수용!)
);
