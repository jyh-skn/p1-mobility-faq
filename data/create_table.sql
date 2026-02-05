USE MENUDB;

CREATE TABLE ParkingLot
(
    id           int primary key AUTO_INCREMENT,
    reg_id       varchar(100) ,
    name         varchar(250),
    lat          varchar(100),
    lng          varchar(100),
    sido         varchar(100),
    sigungu      varchar(100),
    full_address text,
    space_no     int,
    coord        POINT NOT NULL SRID 4326
);

-- 인덱스 추가
CREATE SPATIAL INDEX geo_index ON ParkingLot(coord);
