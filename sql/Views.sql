
CREATE VIEW todayRows AS
SELECT *
FROM ppe_log
WHERE dateAndTime >= CURRENT_TIMESTAMP::date
  AND dateAndTime < (CURRENT_TIMESTAMP + INTERVAL '1 day')::date;

CREATE VIEW allUndetectedObjectRows AS 
SELECT *
FROM ppe_log
WHERE 0 IN (apronCount, bunnysuitCount, maskCount, glovesCount, gogglesCount, headcapCount);

CREATE VIEW todaysAllUndetected AS
SELECT *
FROM ppe_log
WHERE dateAndTime >= CURRENT_TIMESTAMP::date
  AND dateAndTime < (CURRENT_TIMESTAMP + INTERVAL '1 day')::date
  AND 0 IN (apronCount, bunnysuitCount, maskCount, glovesCount, gogglesCount, headcapCount)
;

CREATE VIEW allColumns AS 
SELECT column_name, data_type
FROM (
    SELECT column_name, data_type, 
           ROW_NUMBER() OVER () AS row_num
    FROM information_schema.columns
    WHERE table_schema = 'public' AND table_name = 'ppe_log'
) AS subquery
ORDER BY CASE
    WHEN row_num = 11 THEN 4
    ELSE row_num
END;