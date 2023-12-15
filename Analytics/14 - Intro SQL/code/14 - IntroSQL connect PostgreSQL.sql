-- Получить все доступные нам схемы данных
SELECT schemaname, tablename, tableowner  
FROM pg_catalog.pg_tables
WHERE schemaname != 'pg_catalog' AND 
    schemaname != 'information_schema';
   
-- Получить все доступные схемы данных где владелец 'Student_01'
select schemaname, tablename
from pg_catalog.pg_tables
where tableowner = 'Student_01';


-- Получить имена таблиц для схемы 'bookings'
select tablename
from pg_catalog.pg_tables
where schemaname = 'bookings';

