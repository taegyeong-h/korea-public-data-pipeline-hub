-- CREATE TABLE ods.tm_subway_station_master (
--     station_cd      INT PRIMARY KEY,     -- 역사 코드는 숫자가 효율적이므로 INT 유지
--     station_nm      TEXT NOT NULL,       -- 💡 빅쿼리 STRING처럼 무제한 유동형 문자열
--     route_ln_nm     TEXT NOT NULL,       -- 💡 호선명도 무제한 유동형
--     latitude        DOUBLE PRECISION,    
--     longitude       DOUBLE PRECISION,    
    
--     -- [정보계 감사 컬럼]
--     created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
--     updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
--     is_deleted      TEXT DEFAULT 'N'     -- 💡 이것도 TEXT로 통일
-- );

-- -- 코멘트 등록 (동일)
-- COMMENT ON TABLE ods.tm_subway_station_master IS '지하철 역사별 위치(위경도) 및 호선 기준정보 마스터 테이블';
-- COMMENT ON COLUMN ods.tm_subway_station_master.station_cd IS '역사 고유 코드';
-- COMMENT ON COLUMN ods.tm_subway_station_master.station_nm IS '역사명';
-- COMMENT ON COLUMN ods.tm_subway_station_master.route_ln_nm IS '지하철 호선명';
