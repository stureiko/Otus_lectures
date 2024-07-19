-- Создадим учебную таблицу
-- информация о том какое оборудование брали клиенты в аренду 

--CREATE TABLE IF NOT EXISTS rental (
--  rental_id  INTEGER PRIMARY KEY, 
--  rental_date  DATETIME NOT NULL, 
--  inventory_id  INTEGER NOT NULL,
--  customer_id  INTEGER NOT NULL, 
--  return_date  DATETIME NOT NULL
-- );
-- 
--INSERT INTO rental (rental_id, rental_date, inventory_id, customer_id, return_date )
--VALUES 	(76, '2005-05-25 11:30:37', 3021, 1, '2005-06-03 12:00:37'),
--		(573, '2005-05-28 10:35:23', 4020, 1, '2005-06-03 06:32:23'),
--		(1185, '2005-06-15 00:54:12', 2785, 1, '2005-06-23 02:42:12'),
--		(1422, '2005-06-15 18:02:53', 1021, 1, '2005-06-19 15:54:53'),
--		(1476, '2005-06-15 21:08:46', 1407, 1, '2005-06-25 02:26:46'),
--		(1725, '2005-06-16 15:18:57', 726, 1, '2005-06-17 21:05:57'),
--		(2308, '2005-06-18 08:41:48', 197, 1, '2005-06-22 03:36:48'),
--		(2363, '2005-06-18 13:33:59', 3497,	1, '2005-06-19 17:40:59'),
--		(3284, '2005-06-21 06:24:45', 4566, 1, '2005-06-28 03:28:45'),
--		(4526, '2005-07-08 03:17:05', 1443, 1, '2005-07-14 01:19:05'),
--		(4611, '2005-07-08 07:33:56', 3486, 1, '2005-07-12 13:25:56'),
--		(5244, '2005-07-09 13:24:07', 3726, 1, '2005-07-14 14:01:07'),
--		(5326, '2005-07-09 16:38:01', 797, 1, '2005-07-13 18:02:01'),
--		(6163, '2005-07-11 10:13:46', 1330, 1, '2005-07-19 13:15:46'),
--		(7273, '2005-07-27 11:31:22', 2465, 1, '2005-07-31 06:50:22'),
--		(7841, '2005-07-28 09:04:45', 1092, 1, '2005-07-30 12:37:45'),
--		(8033, '2005-07-28 16:18:23', 4268, 1, '2005-07-30 17:56:23'),
--		(8074, '2005-07-28 17:33:39', 1558, 1, '2005-07-29 20:17:39'),
--		(8116, '2005-07-28 19:20:07', 4497, 1, '2005-07-29 22:54:07'),
--		(8326, '2005-07-29 03:58:49', 108, 1, '2005-08-01 05:16:49'),
--		(9571, '2005-07-31 02:42:18', 2219, 1, '2005-08-02 23:26:18'),
--		(10437, '2005-08-01 08:51:04', 14, 1, '2005-08-10 12:12:04'),
--		(11299, '2005-08-02 15:36:52', 3232, 1, '2005-08-10 16:40:52'),
--		(11367, '2005-08-02 18:01:38', 1440, 1, '2005-08-04 13:19:38'),
--		(11824, '2005-08-17 12:37:54', 2639, 1, '2005-08-19 10:11:54'),
--		(12250, '2005-08-18 03:57:29', 921, 1, '2005-08-22 23:05:29'),
--		(13068, '2005-08-19 09:55:16', 3019, 1, '2005-08-20 14:44:16'),
--		(13176, '2005-08-19 13:56:54', 2269, 1, '2005-08-23 08:50:54'),
--		(14762, '2005-08-21 23:33:57', 4249, 1, '2005-08-23 01:30:57'),
--		(14825, '2005-08-22 01:27:57', 1449, 1, '2005-08-27 07:01:57'),
--		(15298, '2005-08-22 19:41:37', 1446, 1, '2005-08-28 22:49:37'),
--		(15315, '2005-08-22 20:03:46', 312, 1, '2005-08-30 01:51:46');
  

--DELETE 
--FROM rental ;

-- * * * * * * * *	
	
-- Для клиента с customer_id = 1 найдите все периоды, 
-- когда у него был хотя бы один взятый напрокат объект.

-- 1. Посмотрим на исходные данные
	
SELECT *
FROM rental
WHERE customer_id = 1;

-- 2. Нумерация строк и определение «проливов»

-- Воспользуемся оконной функцией row_number(), чтобы для каждой строки вычислить ее порядковый номер 
-- в порядке возврата оборудования в пункт проката. 
-- К сортировке добавим дату начала проката, чтобы в случае одновременного возврата двух объектов первым был тот, что взят ранее.

-- Еще одна оконная функция – lag() – поможет нам для каждой записи получить дату возврата (return_date) из предыдущей строки.

SELECT 
    customer_id,
    ROW_NUMBER () OVER(ORDER BY return_date, rental_date) AS row_num,
    rental_date AS start_date,
    return_date AS finish_date,
    lag(return_date, 1) OVER (ORDER BY return_date, rental_date) AS prev_return_date
FROM rental
WHERE customer_id = 1
ORDER BY row_num;

-- 3. Определение начала новых периодов

-- Из этой таблицы мы можем установить, является ли каждая следующая запись непрерывным продолжением предыдущей. 
-- Для этого нужно убедиться, что дата в колонке prev_return_date больше или равна start_date. 
-- Для удобства записи, воспользуемся CTE (Common Table Expression):

with d as (
    select 
        customer_id,
        row_number() over(order by return_date, rental_date) as row_num,
        rental_date as start_date,
        return_date as finish_date,
        lag(return_date, 1) over (order by return_date, rental_date) as prev_return_date
    from rental
    where customer_id = 1
    order by row_num
) select 
    *,
    case when d.prev_return_date >= start_date then 0 else 1 end new_period
from d;

-- 4. Нумерация «островов»

-- Воспользуемся оконной функцией sum(), чтобы превратить последовательность нулей и единиц в номера периодов («островов»):

with d as (
    select 
        customer_id,
        row_number() over(order by return_date, rental_date) as row_num,
        rental_date as start_date,
        return_date as finish_date,
        lag(return_date, 1) over (order by return_date, rental_date) as prev_return_date
    from rental
    where customer_id = 1
    order by row_num
) select 
    *,
    sum(case when d.prev_return_date >= start_date then 0 else 1 end) over (order by row_num) island_id
from d;

-- 5. Группировка и вывод результата

-- Финальным шагом будет группировка полученного результата по номеру «острова» и 
-- извлечение минимальной даты начала (start_date) и максимальной даты окончания (finish_date) 
-- для каждого периода непрерывной аренды. Для наглядности продолжим использовать CTE-подход:

with d as (
    select 
        customer_id,
        row_number() over(order by return_date, rental_date) as row_num,
        rental_date as start_date,
        return_date as finish_date,
        lag(return_date, 1) over (order by return_date, rental_date) as prev_return_date
    from rental
    where customer_id = 1
    order by row_num
),
islands as (
    select 
        *,
        sum(case when d.prev_return_date >= start_date then 0 else 1 end) over (order by row_num) island_id
    from d
)
select 
    island_id, 
    min(start_date) start_date,
    max(finish_date) finish_date
from islands 
group by island_id ;

