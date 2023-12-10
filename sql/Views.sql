
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

