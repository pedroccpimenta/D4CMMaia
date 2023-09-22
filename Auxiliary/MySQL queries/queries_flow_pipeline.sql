use BAZE;

SELECT DISTINCT(Category) FROM Flow_Categories;

-- SIMPLE QUERIES
SELECT * FROM Flow_Categories WHERE C_G='C115_G1' limit 300 ;

SELECT id, count(*) FROM Flow_Categories WHERE C_G='C115_G1' and id in (
select distinct id from Flow_Categories
) group by id limit 300 ;

select count(*) from Flow_Categories  WHERE C_G='C115_G1';
select count(*) from Flow_Categories  WHERE C_G='C115_G2';
select count(*) from Flow_Categories  WHERE C_G='C115_G3';
select count(*) from Flow_Categories  WHERE C_G='C115_G4';



select min(id) as min, max(id) as max, max(id)-min(id) from Flow_Categories  WHERE C_G='C115_G1';





SELECT category, count(*) FROM Flow_Categories WHERE C_G='C115_G1' and category in (
select distinct category from Flow_Categories
) group by category limit 300 ;





SELECT * FROM Flow_Distribution WHERE End_datetime >= '2022-08-23' AND End_datetime <= '2022-08-24' AND C_G = 'C115_G1';
SELECT * FROM Flow_Distribution WHERE C_G='C115_G3' ORDER BY End_datetime ASC limit 100;

-- DATE CONVERSION 
ALTER TABLE Flow_Distribution ADD End_datetime DATETIME NULL; 
UPDATE Flow_Distribution SET End_datetime = FROM_UNIXTIME(End_timestamp_epoch/1000) WHERE End_timestamp_epoch IS NOT NULL;

-- ALTER TABLE TO ADD Created_By
ALTER TABLE Flow_Distribution;
UPDATE Flow_Distribution SET Created_By = 'eferreira';

-- QUERY FLOW DISTRIBUTION
select C_G, DATE(Start_datetime), DATE(End_datetime), Bicycle, Bus, Car, Heavy, Light, Motorcycle 
from BAZE.Flow_Distribution 
where DATE(Start_datetime) >= '2022-07-01' and DATE(End_datetime) <= '2022-11-09' ;

select distinct(C_G) from Flow_Distribution  order by C_G asc;

SELECT * FROM Flow_Distribution;

select C_G, DATE(Start_datetime) as Start_datetime, DATE(End_datetime) as End_datetime, Bicycle, Bus, Car, Heavy, Light, Motorcycle from BAZE.Flow_Distribution where C_G = 'C115_G2' and DATE(Start_datetime) >= '2022-07-01' and DATE(End_datetime) <= '2022-11-09 11:35:23' order by End_datetime desc limit 10 ;


-- QUERY FLOW CATEGORIES
select C_G, Category, DATE(Trajectory_start_datetime), DATE(Trajectory_end_datetime), Average_speed_kpxh, Duration_of_occurrence_s, Stationary_duration_s 
from BAZE.Flow_Categories
where DATE(Trajectory_start_datetime) >= '2022-10-08' and DATE(Trajectory_end_datetime) <= '2022-10-25' and Category = 'bus' ORDER BY Trajectory_end_datetime DESC;

select C_G, (select Average_speed_kpxh from BAZE.Flow_Categories where Category = 'bicycle') as Bicycle, 
(select category from BAZE.Flow_Categories where Category = 'bus' limit 1) as Bus, 
(select category from BAZE.Flow_Categories where Category = 'car' limit 1) as Car, 
(select category from BAZE.Flow_Categories where Category = 'heavy' limit 1) as Heavy, 
(select category from BAZE.Flow_Categories where Category = 'light' limit 1) as Light, 
(select category from BAZE.Flow_Categories where Category = 'motorcycle' limit 1) as Motorcycle,
DATE(Trajectory_start_datetime), DATE(Trajectory_end_datetime), Average_speed_kpxh, Duration_of_occurrence_s, Stationary_duration_s 
from BAZE.Flow_Categories
where DATE(Trajectory_start_datetime) >= '2022-10-08' and DATE(Trajectory_end_datetime) <= '2022-10-25';




select Average_speed_kpxh as bike, Duration_of_occurrence_s, Stationary_duration_s  from BAZE.Flow_Categories where Category = 'bicycle';

SELECT C_G, DATE(Start_datetime) as Start_datetime, End_datetime AS End_datetime, Bicycle, Bus, Car, Heavy, Light, Motorcycle FROM BAZE.Flow_Distribution WHERE C_G = 'C115_G1' AND DATE(Start_datetime) >= '2022-07-01' and DATE(End_datetime) <= '2022-11-16 11:22:52' order by End_datetime;
SELECT distinct Category from BAZE.Flow_Categories

-- OTHER
-- SET GLOBAL local_infile = 1
-- SET SQL_SAFE_UPDATES = 0