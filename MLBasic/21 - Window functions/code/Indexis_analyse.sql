-- Show tables in otus_demo shema

select tablename
from pg_catalog.pg_tables
where schemaname = 'otus_demo';

-- create a new simple table

CREATE TABLE IF NOT EXISTS foo (c1 integer, c2 text);


-- insert 1e6 rows
INSERT INTO foo
  SELECT i, md5(random()::text)
  FROM generate_series(1, 1000000) AS i;
  
 
SELECT * FROM foo f
LIMIT 10;

SELECT count(*) FROM foo;

-- explain query
EXPLAIN SELECT * FROM foo;

-- analyse query
EXPLAIN (ANALYSE) SELECT * FROM foo;

-- analyse query with buffers
-- Buffers: shared hit - blocks read from cash 
EXPLAIN (ANALYSE, BUFFERS ) SELECT * FROM foo;

SELECT * 
FROM foo 
WHERE c1 > 500
AND c1 < 2000;

-- analyse query with two conditions
EXPLAIN (ANALYSE) 
SELECT * 
FROM foo 
WHERE c1 > 500
AND c1 < 2000;

EXPLAIN (ANALYSE, SETTINGS) 
SELECT * 
FROM foo 
WHERE c1 > 500
AND c1 < 2000;

-- create index
CREATE INDEX ON foo(c1);

-- compare time of query execution
EXPLAIN (analyse) 
SELECT * 
FROM foo 
WHERE c1 > 500
AND c1 < 2000;

-- show list of DB indexies
select *
from pg_indexes
where tablename = 'foo';

-- drop index foo_c1_idx
DROP INDEX foo_c1_idx;

CREATE TABLE "employee" (
    id uuid primary key,
    name text,
    department text
);

CREATE TABLE "employee_contact" (
    id uuid primary key,
    contact_number int not null,
    employee_id uuid unique not null
    references "employee" (id) on delete CASCADE ON UPDATE CASCADE 
);

DROP TABLE "employee_contact";

DROP TABLE "employee";









