-- CREATE TABLE dw.tt_seoul_subway_stats_monthly (
--      use_mm          VARCHAR(6) NOT NULL,
--      sbwy_rout_ln_nm VARCHAR(50) NOT NULL,
--      sttn            VARCHAR(100) NOT NULL,
--      hr_0_get_on_nope   NUMERIC, hr_0_get_off_nope  NUMERIC,
--      hr_1_get_on_nope   NUMERIC, hr_1_get_off_nope  NUMERIC,
--      hr_2_get_on_nope   NUMERIC, hr_2_get_off_nope  NUMERIC,
--      hr_3_get_on_nope   NUMERIC, hr_3_get_off_nope  NUMERIC,
--      hr_4_get_on_nope   NUMERIC, hr_4_get_off_nope  NUMERIC,
--      hr_5_get_on_nope   NUMERIC, hr_5_get_off_nope  NUMERIC,
--      hr_6_get_on_nope   NUMERIC, hr_6_get_off_nope  NUMERIC,
--      hr_7_get_on_nope   NUMERIC, hr_7_get_off_nope  NUMERIC,
--      hr_8_get_on_nope   NUMERIC, hr_8_get_off_nope  NUMERIC,
--      hr_9_get_on_nope   NUMERIC, hr_9_get_off_nope  NUMERIC,
--      hr_10_get_on_nope  NUMERIC, hr_10_get_off_nope NUMERIC,
--      hr_11_get_on_nope  NUMERIC, hr_11_get_off_nope NUMERIC,
--      hr_12_get_on_nope  NUMERIC, hr_12_get_off_nope NUMERIC,
--      hr_13_get_on_nope  NUMERIC, hr_13_get_off_nope NUMERIC,
--      hr_14_get_on_nope  NUMERIC, hr_14_get_off_nope NUMERIC,
--      hr_15_get_on_nope  NUMERIC, hr_15_get_off_nope NUMERIC,
--      hr_16_get_on_nope  NUMERIC, hr_16_get_off_nope NUMERIC,
--      hr_17_get_on_nope  NUMERIC, hr_17_get_off_nope NUMERIC,
--      hr_18_get_on_nope  NUMERIC, hr_18_get_off_nope NUMERIC,
--      hr_19_get_on_nope  NUMERIC, hr_19_get_off_nope NUMERIC,
--      hr_20_get_on_nope  NUMERIC, hr_20_get_off_nope NUMERIC,
--      hr_21_get_on_nope  NUMERIC, hr_21_get_off_nope NUMERIC,
--      hr_22_get_on_nope  NUMERIC, hr_22_get_off_nope NUMERIC,
--      hr_23_get_on_nope  NUMERIC, hr_23_get_off_nope NUMERIC,
--      job_ymd         DATE,
--      last_updated    TIMESTAMP NOT NULL,
--      PRIMARY KEY (use_mm, sbwy_rout_ln_nm, sttn)
--  );




INSERT INTO dw.tt_seoul_subway_stats_monthly (
use_mm, sbwy_rout_ln_nm, sttn,
    hr_0_get_on_nope,  hr_0_get_off_nope,  hr_1_get_on_nope,  hr_1_get_off_nope,
    hr_2_get_on_nope,  hr_2_get_off_nope,  hr_3_get_on_nope,  hr_3_get_off_nope,
    hr_4_get_on_nope,  hr_4_get_off_nope,  hr_5_get_on_nope,  hr_5_get_off_nope,
    hr_6_get_on_nope,  hr_6_get_off_nope,  hr_7_get_on_nope,  hr_7_get_off_nope,
    hr_8_get_on_nope,  hr_8_get_off_nope,  hr_9_get_on_nope,  hr_9_get_off_nope,
    hr_10_get_on_nope, hr_10_get_off_nope, hr_11_get_on_nope, hr_11_get_off_nope,
    hr_12_get_on_nope, hr_12_get_off_nope, hr_13_get_on_nope, hr_13_get_off_nope,
    hr_14_get_on_nope, hr_14_get_off_nope, hr_15_get_on_nope, hr_15_get_off_nope,
    hr_16_get_on_nope, hr_16_get_off_nope, hr_17_get_on_nope, hr_17_get_off_nope,
    hr_18_get_on_nope, hr_18_get_off_nope, hr_19_get_on_nope, hr_19_get_off_nope,
    hr_20_get_on_nope, hr_20_get_off_nope, hr_21_get_on_nope, hr_21_get_off_nope,
    hr_22_get_on_nope, hr_22_get_off_nope, hr_23_get_on_nope, hr_23_get_off_nope,
    job_ymd, last_updated
)
SELECT 
use_mm, sbwy_rout_ln_nm, sttn,
    hr_0_get_on_nope,  hr_0_get_off_nope,  hr_1_get_on_nope,  hr_1_get_off_nope,
    hr_2_get_on_nope,  hr_2_get_off_nope,  hr_3_get_on_nope,  hr_3_get_off_nope,
    hr_4_get_on_nope,  hr_4_get_off_nope,  hr_5_get_on_nope,  hr_5_get_off_nope,
    hr_6_get_on_nope,  hr_6_get_off_nope,  hr_7_get_on_nope,  hr_7_get_off_nope,
    hr_8_get_on_nope,  hr_8_get_off_nope,  hr_9_get_on_nope,  hr_9_get_off_nope,
    hr_10_get_on_nope, hr_10_get_off_nope, hr_11_get_on_nope, hr_11_get_off_nope,
    hr_12_get_on_nope, hr_12_get_off_nope, hr_13_get_on_nope, hr_13_get_off_nope,
    hr_14_get_on_nope, hr_14_get_off_nope, hr_15_get_on_nope, hr_15_get_off_nope,
    hr_16_get_on_nope, hr_16_get_off_nope, hr_17_get_on_nope, hr_17_get_off_nope,
    hr_18_get_on_nope, hr_18_get_off_nope, hr_19_get_on_nope, hr_19_get_off_nope,
    hr_20_get_on_nope, hr_20_get_off_nope, hr_21_get_on_nope, hr_21_get_off_nope,
    hr_22_get_on_nope, hr_22_get_off_nope, hr_23_get_on_nope, hr_23_get_off_nope,
    job_ymd, CURRENT_TIMESTAMP
FROM ods.tt_seoul_subway_stats_monthly
