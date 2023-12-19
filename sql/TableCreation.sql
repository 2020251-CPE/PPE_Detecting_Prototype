---postgreSQL main table
CREATE TABLE ppe_log (
    id              SERIAL PRIMARY KEY,
    photoName       VARCHAR(255) NOT NULL,
    photoURL        VARCHAR(255) NOT NULL,
    dateAndTime     TIMESTAMP NOT NULL,
    apronCount      INT NOT NULL,
    bunnysuitCount  INT NOT NULL,
    maskCount       INT NOT NULL,
    glovesCount     INT NOT NULL,
    gogglesCount    INT NOT NULL,
    headcapCount    INT NOT NULL
);

ALTER TABLE ppe_log
ADD hostName VARCHAR(50);