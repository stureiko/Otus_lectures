-- Создадим новую БД SQLite (локальный файл)
-- через Database manager

-- Создаем таблицы 
CREATE TABLE IF NOT EXISTS employees (
  id  INTEGER PRIMARY KEY, 
  name  TEXT NOT NULL, 
  city  TEXT NOT NULL,
  department  TEXT NOT NULL, 
  salary  INTEGER NOT NULL
  );
 
 CREATE TABLE IF NOT EXISTS expenses (
  year  INTEGER NOT NULL , 
  month INTEGER NOT NULL, 
  income INTEGER NOT NULL,
  expense INTEGER NOT NULL 
  );
 
-- заполняем данными
INSERT INTO
  employees (id, name, city, department, salary)
VALUES
  (11,'Дарья','Самара','hr',70),
  (12,'Борис','Самара','hr',78),
  (21,'Елена','Самара','it',84),
  (22,'Ксения','Москва','it',90),
  (23,'Леонид','Самара','it',104),
  (24,'Марина','Москва','it',104),
  (25,'Иван','Москва','it',120),
  (31,'Вероника','Москва','sales',96),
  (32,'Григорий','Самара','sales',96),
  (33,'Анна','Москва','sales',100); 
 
 INSERT INTO
  expenses (year, month, income, expense)
VALUES
( 2020 , 1     , 94     , 82      ),
( 2020 , 2     , 94     , 75      ),
( 2020 , 3     , 94     , 104     ),
( 2020 , 4     , 100    , 94      ),
( 2020 , 5     , 100    , 99      ),
( 2020 , 6     , 100    , 105     ),
( 2020 , 7     , 100    , 95      ),
( 2020 , 8     , 100    , 110     ),
( 2020 , 9     , 104    , 104     );
  
SELECT *
FROM employees;

SELECT *
FROM expenses;

-- Ранжирование

-- Отсортируем таблицу по зарплате 
SELECT
  name, department, salary
FROM employees
ORDER BY salary DESC;

-- создаем ранг

-- window — ключевое слово, которое показывает, что дальше будет определение окна;
-- w — название окна (может быть любым);
-- (order by salary desc) — описание окна («значения столбца salary, упорядоченные по убыванию»)
SELECT
  DENSE_RANK() OVER w AS rank,
  name, department, salary
FROM employees
WINDOW w AS (ORDER BY salary DESC)
ORDER BY rank;

SELECT
  DENSE_RANK() OVER w AS rank,
  name, department, salary
FROM employees
WINDOW w AS (ORDER BY department)
ORDER BY rank;

SELECT
  RANK() OVER w AS rank,
  name, department, salary
FROM employees
WINDOW w AS (ORDER BY department)
ORDER BY rank;

-- Рейтинг зарплат по департаментам

-- 1. Сначала отсортируем таблицу по департаментам, а внутри департамента — по убыванию зарплаты
SELECT
  name, department, salary
FROM employees
ORDER BY department, salary DESC;


-- Теперь создадим ранг внутри каждого департамента по зарплате
-- partition by department указывает, как следует разбить окно на секции;
-- order by salary desc задает сортировку внутри секции.
-- Функция расчета ранга остается прежней — dense_rank().
SELECT 
  DENSE_RANK() OVER w AS rank,
  name, department, salary
FROM employees
WINDOW w AS (
  PARTITION BY department
  ORDER BY salary DESC
)
ORDER BY department, rank;


-- Сформируем группы по зарплате

-- отсортируем по зарплате
SELECT name, department, salary
FROM employees e
ORDER BY salary DESC;

-- ntile(n) разбивает все записи на n групп и возвращает номер группы для каждой записи. 
-- Если общее количество записей (10 в нашем случае) не делится на размер группы (3), 
-- то первые группы будут крупнее последних.
SELECT 
	ntile(3) OVER w AS tile,
	name, department, salary
FROM employees
WINDOW w AS (ORDER BY salary DESC)
ORDER BY salary DESC;


-- Смещение

-- разница зарплаты с предыдущим
-- Чтобы на каждом шаге подтягивать зарплату предыдущего сотрудника, 
-- будем использовать оконную функцию lag()

-- Функция lag() возвращает значение из указанного столбца, 
-- отстоящее от текущего на указанное количество записей назад. 
-- В нашем случае — salary от предыдущей записи.
SELECT 
  id, name, department, salary,
  lag(salary, 1) OVER w AS prev
FROM employees
WINDOW w AS (ORDER BY salary)
ORDER BY salary;


-- Осталось посчитать разницу между prev и salary в процентах
SELECT
  name, department, salary,
  round(
    		(salary - lag(salary, 1) over w)*100.0 / salary
  		) || '%' AS diff
FROM employees
WINDOW w AS (ORDER BY salary)
ORDER BY salary;


-- Диапазон зарплат в департаменте
-- Сначала отсортируем таблицу по департаментам, а внутри департамента — по возрастанию зарплаты
SELECT
  name, department, salary,
  NULL AS low,
  NULL AS high
FROM employees
ORDER BY department, salary;

-- first_value() — зарплата первого сотрудника, входящего в секцию окна;
-- last_value() — зарплата последнего сотрудника, входящего в секцию.
SELECT
  name, department, salary,
  first_value(salary) OVER w AS low,
  last_value(salary) OVER w AS high
FROM employees
WINDOW w AS (
  PARTITION BY department
  ORDER BY salary
)
ORDER BY department, salary;

-- Упс... проблема
-- low рассчитался корректно, а вот с high какая-то ерунда. 
-- Вместо того, чтобы равняться максимальной зарплате департамента, он меняется от сотрудника к сотруднику.
-- Дело в том, что функции first_value() и last_value() работают не просто с секцией окна. 
-- Они работают с фреймом внутри секции:
-- Чтобы last_value() работала как мы ожидаем, придется «прибить» границы фрейма к границам секции. 
-- Тогда для каждой секции фрейм будет в точности совпадать с ней
SELECT
  name, department, salary,
  first_value(salary) OVER w AS low,
  last_value(salary) OVER w AS high
FROM employees
WINDOW w AS (
  PARTITION BY department
  ORDER BY salary
  rows between 
  		unbounded preceding 
  and 	unbounded FOLLOWING  -- задаем фрейм обработки на все партицию
	)
ORDER BY department, salary, id;

-- Агрегация
-- посмотрим на сумму и % зарплат по департаментам
SELECT
  name, department, salary,
  sum(salary) OVER w AS fund,
  round(salary * 100.0 / sum(salary) OVER w) || ' %' AS perc
FROM employees
WINDOW w AS (PARTITION BY department)
ORDER BY department, salary, id;

-- Сделаем сравнение со средней зарплатой
SELECT
  name, department, salary,
  round(avg(salary) OVER w) AS avg_sal,
  round((salary - avg(salary) OVER w)*100.0 / round(avg(salary) OVER w)) AS diff
FROM employees
WINDOW 
	w AS (PARTITION BY department)
ORDER BY department, salary, id;

-- Несколько окон внутри запроса

-- Сделаем сравнение со средней зарплатой
-- и посмотрим какой % она составляет от общего фонда зарплат
SELECT
  name, department, salary,
  round(salary * 100 / sum(salary) OVER t) || '%' AS perc_total,
  round(avg(salary) OVER w) AS avg_sal,
  round((salary - avg(salary) OVER w)*100.0 / round(avg(salary) OVER w)) AS diff
FROM employees
WINDOW 
	w AS (PARTITION BY department),
	t AS ()
ORDER BY department, salary, id;


-- Скользящие агрегаты

-- Подготовим шаблон
SELECT
  year, month, expense,
  NULL AS roll_avg
FROM expenses
ORDER BY year, month;

-- Нужно задать определение фрейма: «выбрать строки от 1 предыдущей до 1 следующей»
SELECT
  year, month, expense,
  round(avg(expense) OVER w) AS roll_avg
FROM expenses
WINDOW w AS (
  ORDER BY year, month
  rows between 
  		1 preceding 
  	and 1 FOLLOWING  -- задаем фрейм обработки [+1, -1] строка
)
ORDER BY year, month;

-- Кумулятивная сумма
-- Функция rows between unbounded preceding and current row позволяет 
-- последовательно увеличивать фрейм для суммирования данных и получения нарастающей суммы
SELECT
  year, month, income, expense,
  sum(income) OVER w AS cum_income,
  sum(expense) OVER w AS cum_expense,
  (sum(income) OVER w) - (sum(expense) OVER w) AS cum_profit,
  round(avg(income) OVER w) AS cum_avg,
  round(avg(income) OVER w) + (sum(income) OVER w) - (sum(expense) OVER w) AS avg_profit
FROM expenses
WINDOW w AS (
  ORDER BY year, month
  rows between 
  		unbounded preceding 
  	and current row
)
ORDER BY year, month;



