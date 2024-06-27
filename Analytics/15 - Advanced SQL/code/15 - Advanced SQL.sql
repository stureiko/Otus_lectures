
SELECT schemaname, tablename, tableowner  
FROM pg_catalog.pg_tables
WHERE schemaname != 'pg_catalog' AND 
    schemaname != 'information_schema';

    
select schemaname, tablename
from pg_catalog.pg_tables
where tableowner = 'Student_01';


select tablename
from pg_catalog.pg_tables
where schemaname = 'bookings';


-- ПОДЗАПРОСЫ

-- Выбрать номера билетов 
-- стоимость которых выше среднего

-- 1. Получим средню стоимост билета
SELECT avg(amount)
FROM ticket_flights tf;

-- 2. Применим фильтрацию по этому значению
SELECT * 
FROM ticket_flights tf 
WHERE amount > (SELECT avg(amount)
				FROM ticket_flights tf)
LIMIT 10;


-- EXISTS

SELECT b.*
FROM bookings b 
WHERE EXISTS (	SELECT *
				FROM tickets t 
				WHERE b.book_ref = t.book_ref AND b.total_amount > 100000)
ORDER BY b.book_ref 
LIMIT 10;
			

SELECT b.*
FROM bookings b 
INNER JOIN tickets t 
ON b.book_ref = t.book_ref 
WHERE b.total_amount > 100000
ORDER BY b.book_ref
LIMIT 10;

			
-- Найти рейсы на которых были билеты бизнесс-класса

-- Найдем все самолеты на которых есть билеты бизнесс-класса
SELECT aircraft_code
FROM seats s
WHERE fare_conditions = 'Business';

-- Объединим с таблицей полетов
SELECT flight_no, scheduled_departure, scheduled_arrival, aircraft_code
FROM flights f
WHERE aircraft_code IN (
    SELECT aircraft_code
    FROM seats s
    WHERE fare_conditions = 'Business'
);

SELECT *
FROM seats s 
WHERE aircraft_code IN (
	SELECT aircraft_code  
	FROM aircrafts a 
	WHERE model LIKE 'Boeing%')
ORDER BY aircraft_code
LIMIT 10;

-- соединение таблиц JOIN

-- полчить номера билетов которые были проданы 
-- пассажиру Vladimir с 1 по 6 июня 2017 года
SELECT t.ticket_no, t.passenger_name, b.book_date
FROM tickets t
JOIN bookings b
ON t.book_ref = b.book_ref
AND b.book_date >= '2017-06-01'
AND b.book_date <= '2017-06-07'
AND t.passenger_name LIKE '%VLADIMIR%'
ORDER BY b.book_date 
LIMIT 10 ;


-- получить посадочные места, проданные Vladimir'y в бизнесс-класс
-- на рейсы из Москвы в период с 1 по 5 июня 2017 года
-- 0. Что у нас вообще есть в таблице airports_data
SELECT * 
FROM airports_data ad 
LIMIT 10;


-- 1. Получим коды московских аэропортов
SELECT ad.airport_code, * 
FROM airports_data ad 
WHERE ad.city @> '{"en": "Moscow"}'  -- распаковка json
LIMIT 10;

-- 2. Получим все рейсы вылетащющие из Москвы
SELECT DISTINCT f.flight_no, f.departure_airport AS airport_code 
FROM flights f 
JOIN airports_data ad 
ON f.departure_airport = ad.airport_code 
WHERE f.departure_airport IN 
	(SELECT ad.airport_code 
 	 FROM airports_data ad 
	 WHERE ad.city @> '{"en": "Moscow"}')  -- распаковка json
ORDER BY f.flight_no
LIMIT 10;

-- или по другому
SELECT DISTINCT f.flight_no, f.departure_airport AS airport_code
FROM flights f
INNER JOIN airports a
ON f.departure_airport = a.airport_code 
AND a.city = 'Moscow'
ORDER BY f.flight_no
LIMIT 10;

-- 3. Получим все рейсы вылетащющие из Москвы
-- на которых был бизнесс-класс
SELECT DISTINCT f.flight_no, f.status, tf.fare_conditions 
FROM flights f 
JOIN airports_data ad 
ON f.departure_airport = ad.airport_code 
JOIN ticket_flights tf 
ON f.flight_id = tf.flight_id 
WHERE f.departure_airport IN 
	(SELECT ad.airport_code 
 	 FROM airports_data ad 
	 WHERE ad.city @> '{"en": "Moscow"}')
AND tf.fare_conditions = 'Business'
LIMIT 10;


-- 4. Соберем итоговую конструкцию
SELECT 	bp.seat_no, 
		tf.fare_conditions, 
		t.passenger_name, 
		f.scheduled_departure, 
		f.departure_airport, 
		f.arrival_airport
FROM boarding_passes bp 
JOIN ticket_flights tf 
	ON bp.ticket_no = tf.ticket_no 
JOIN tickets t 
	ON tf.ticket_no = t.ticket_no
JOIN flights f 
	ON tf.flight_id = f.flight_id 
WHERE tf.fare_conditions = 'Business'
	AND t.passenger_name LIKE '%VLADIMIR%'
	AND f.scheduled_departure >= '2017-06-01'
	AND f.scheduled_departure <= '2017-06-06'
	AND f.departure_airport IN 
		(SELECT ad.airport_code 
	 	 FROM airports_data ad 
		 WHERE ad.city @> '{"en": "Moscow"}')
ORDER BY f.scheduled_departure ;


-- Посчитаем количество рейсов с определенными номерами
SELECT flight_no, count(flight_no) 
FROM flights f
GROUP BY flight_no 
LIMIT 10;

-- Добавим фильтрацию
SELECT flight_no, count(flight_no) 
FROM flights f
GROUP BY flight_no 
HAVING flight_no IN ('PG0001', 'PG0002', 'PG0003')
LIMIT 10;


-- Объединение результатов UNION
-- Объединение таблиц оператором UNION выполняется для таблиц никак не связанных, но со схожей структурой.

-- выбрать номера рейсов, которые вылетали или прилетали в московские аэропорты 

-- 1. выбрать номера рейсов, которые вылетали из Москвы
SELECT flight_no, departure_airport AS airport_code, 'departure' AS depart_or_arrive
FROM flights f
INNER JOIN airports a
ON f.departure_airport = a.airport_code and a.city = 'Moscow'
LIMIT 10;

-- 2. выбрать номера рейсов, которые прилетали в Москву
SELECT flight_no, arrival_airport AS airport_code, 'arrival' AS depart_or_arrive
FROM flights f
INNER JOIN airports a
ON f.arrival_airport = a.airport_code and a.city = 'Moscow'
LIMIT 10;


-- 3. соберем все вместе
SELECT flight_no, departure_airport AS airport_code, 'departure' AS depart_or_arrive
FROM flights f
INNER JOIN airports a
ON f.departure_airport = a.airport_code and a.city = 'Moscow'
UNION
SELECT flight_no, arrival_airport AS airport_code, 'arrival' AS depart_or_arrive
FROM flights f
INNER JOIN airports a
ON f.arrival_airport = a.airport_code and a.city = 'Moscow';


-- HAVING and WHERE

SELECT flight_no, count(flight_no) 
FROM flights f
GROUP BY flight_no 
HAVING count(flight_no) > 20
ORDER BY flight_no;


SELECT flight_no, count(flight_no) 
FROM flights f
WHERE f.status = 'Scheduled'
GROUP BY flight_no 
HAVING count(flight_no) > 20
ORDER BY flight_no;
