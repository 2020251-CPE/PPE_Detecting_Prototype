---postgreSQL main table
CREATE TABLE ppe_log (
    id              SERIAL PRIMARY KEY,
    photoName       VARCHAR(255) NOT NULL,
    photoURL        VARCHAR(255) NOT NULL,
    dateAndTime     DATETIME NOT NULL,
    apronCount      INT NOT NULL,
    bunnysuitCount  INT NOT NULL,
    gasmaskCount    INT NOT NULL,
    glovesCount     INT NOT NULL,
    gogglesCount    INT NOT NULL,
    headcapCount    INT NOT NULL
);