-- Получить все доступные нам схемы данных
SELECT schemaname, tablename, tableowner  
FROM pg_catalog.pg_tables
WHERE schemaname != 'pg_catalog' AND 
    schemaname != 'information_schema';
   
-- Получить все доступные схемы данных где владелец 'Student_01'
SELECT schemaname, tablename
FROM pg_catalog.pg_tables
WHERE tableowner = 'Student_01';


-- Получить имена таблиц для схемы 'bookings'
SELECT tablename
FROM pg_catalog.pg_tables
WHERE schemaname = 'bookings';


-- Получить все поля определенной таблицы
SELECT column_name 
FROM information_schema.columns 
WHERE table_schema = 'bookings'
  AND table_name   = 'flights';
 
 

-- или так
SELECT *
FROM flights f 
LIMIT 0;

-- Получить все данные из таблицы
-- Внимание, вы пока не занете сколько там данных и это может "подвесить" вашу сессию работы
SELECT *
FROM flights f 
LIMIT 100;

-- Давайте узнаем сколько строк содержит наша таблица
SELECT count(*)
FROM flights f ;

-- Переименуем столбец результата. Дальше это нам понадобиться, чтобы выводить
-- осмыссленные результаты 
SELECT count(*) AS "number of notes"
FROM flights f ;

-- Обратите внимание, в отличии от Python'a SQL требует от нас двойные кавычки
-- такой код вызовет ошибку
SELECT count(*) AS 'number of notes'
FROM flights f ;

SELECT flight_no, departure_airport AS depart
FROM flights f 
LIMIT 100;

-- Получим первые 100 записей
SELECT *
FROM seats
LIMIT 100;

-- Получим посление 100 записей
SELECT *
FROM seats s
ORDER BY DESC 
LIMIT 100;

-- А по какому критерию они "последние"?
-- Например по коду рейса
SELECT *  
FROM seats s 
ORDER BY aircraft_code DESC  
LIMIT 100;

-- Получить коды рейсов
SELECT aircraft_code
FROM seats s ;
-- Упс... Хочу без повторов

-- Получить только УНИКАЛЬНЫЕ коды рейсов без повторов
SELECT DISTINCT aircraft_code
FROM seats s ;

-- Давайте отсортируем и сделаем по возрастанию
SELECT DISTINCT aircraft_code
FROM seats s 
ORDER BY aircraft_code ;

-- Фильтрация
-- выберем только места, которые обслуживают бизнесс-класс
SELECT DISTINCT seat_no  
FROM seats s 
WHERE fare_conditions = 'Business'
ORDER BY seat_no
LIMIT 100;

--  Выберем рейсы и выведем их номера где были билеты бизнесс-класса
SELECT DISTINCT aircraft_code 
FROM seats s 
WHERE fare_conditions = 'Business'
ORDER BY aircraft_code
LIMIT 100;

-- Выберем рейсы на которых ТОЛЬКО билеты эконом-класса
-- так просто это сделат не удасться
-- Оператор WHERE фильтрует строки до группировки, 
-- а для решения этой задачи требуется анализировать данные на уровне групп (по каждому номеру рейса)
-- приведу пример - а обсудим его на следующем семинаре
SELECT DISTINCT aircraft_code
FROM seats
GROUP BY aircraft_code
HAVING SUM(CASE WHEN fare_conditions = 'Economy' THEN 1 ELSE 0 END) > 0
   AND SUM(CASE WHEN fare_conditions IN ('Business', 'Comfort') THEN 1 ELSE 0 END) = 0 ;
  
-- Фильтрация по подстроке
SELECT *
FROM tickets t 
WHERE passenger_name LIKE '%SERGEEVA'
LIMIT 100;

SELECT count(*)
FROM tickets t 
WHERE passenger_name LIKE '%SERGEEVA'
LIMIT 100;

-- Фильтрация по подстроке
-- Не забывайте про LIMIT 
-- потому что результат может быть не ожиданным
-- например в этой таблице Елен - более 25 тысяч
SELECT count(*)
FROM tickets t 
WHERE passenger_name LIKE '%ELENA%'
LIMIT 100;

-- Аэропорты, которые содержат слово International и находятся в Европе
-- отсортировать по городу по возрастанию и потом по коду по убыванию


SELECT *
FROM airports a 
WHERE airport_name LIKE '%International%'
	AND timezone LIKE 'Europe%'
ORDER BY city ASC, airport_code DESC
LIMIT 100;

-- Посчитать сколько аэропортов находится в городах 
SELECT city, count(airport_name) AS num
FROM airports a 
GROUP BY city ;

-- и вывести только те где больше 1
SELECT city, count(airport_name) AS num
FROM airports a 
GROUP BY city 
HAVING count(airport_name) > 1;

SELECT count(*)
FROM bookings b 
LIMIT 100;

-- посчитать сколько было бронирований билетов суммарно по датам
-- и вывести 20 наиболее "продажных"
SELECT book_date, sum(total_amount) AS summa
FROM bookings b 
GROUP BY book_date 
ORDER BY sum(total_amount) DESC
LIMIT 20;

-- Посчитать сколько было бронирований по месяцам
-- в PostgreSQL можно воспользоваться функцией date_trunc. 
-- Эта функция позволяет усечь дату до указанного компонента, такого как месяц, год и т.д.
SELECT  date_trunc('month', book_date) AS month, 
		sum(total_amount) AS total_sales
FROM bookings
GROUP BY date_trunc('month', book_date)
ORDER BY month
LIMIT 100;

-- Посчитать сколько было бронирований по часам
SELECT  date_trunc('hour', book_date) AS hour, 
		SUM(total_amount) AS total_sales
FROM bookings
GROUP BY date_trunc('hour', book_date)
ORDER BY hour
LIMIT 100;

-- Упс... а нужны были ТОЛЬКО часы суток без даты

-- Посчитать сколько было бронирований по часам без указания суток
SELECT EXTRACT('hour' FROM book_date) AS hour, SUM(total_amount) AS total_sales
FROM bookings
GROUP BY EXTRACT('hour' FROM book_date)
ORDER BY hour
LIMIT 100;


