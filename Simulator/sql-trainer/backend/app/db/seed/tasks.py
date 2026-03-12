"""
Начальные задания для SQL-тренажера.
Запускается при старте приложения если таблица tasks пуста.
"""
import json

TASKS = [
    {
        "title": "Выбрать всех пользователей",
        "description": (
            "Напишите запрос, который возвращает **все столбцы** из таблицы `users`."
        ),
        "difficulty": "easy",
        "topic": "SELECT",
        "order_num": 1,
        "reference_sql": "SELECT * FROM users",
        "db_schema_sql": """
            CREATE TABLE users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                age INTEGER
            );
        """,
        "db_seed_sql": """
            INSERT INTO users VALUES (1, 'Алиса', 'alice@example.com', 25);
            INSERT INTO users VALUES (2, 'Боб', 'bob@example.com', 30);
            INSERT INTO users VALUES (3, 'Карл', 'carl@example.com', 22);
        """,
        "order_matters": False,
        "hints": json.dumps(["Используйте SELECT * для выбора всех столбцов."]),
    },
    {
        "title": "Имена и возраст пользователей старше 24",
        "description": (
            "Верните столбцы `name` и `age` из таблицы `users` "
            "только для пользователей, чей возраст **больше 24**. "
            "Отсортируйте результат по возрасту по убыванию."
        ),
        "difficulty": "easy",
        "topic": "WHERE",
        "order_num": 2,
        "reference_sql": "SELECT name, age FROM users WHERE age > 24 ORDER BY age DESC",
        "db_schema_sql": """
            CREATE TABLE users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                age INTEGER
            );
        """,
        "db_seed_sql": """
            INSERT INTO users VALUES (1, 'Алиса', 'alice@example.com', 25);
            INSERT INTO users VALUES (2, 'Боб', 'bob@example.com', 30);
            INSERT INTO users VALUES (3, 'Карл', 'carl@example.com', 22);
        """,
        "order_matters": True,
        "hints": json.dumps([
            "Используйте WHERE age > 24 для фильтрации.",
            "Используйте ORDER BY age DESC для сортировки по убыванию.",
        ]),
    },
    {
        "title": "Количество заказов по пользователям",
        "description": (
            "Подсчитайте количество заказов для каждого пользователя. "
            "Верните `user_id` и количество заказов с псевдонимом `order_count`. "
            "Отсортируйте по убыванию количества заказов."
        ),
        "difficulty": "medium",
        "topic": "GROUP BY",
        "order_num": 3,
        "reference_sql": (
            "SELECT user_id, COUNT(*) AS order_count "
            "FROM orders "
            "GROUP BY user_id "
            "ORDER BY order_count DESC"
        ),
        "db_schema_sql": """
            CREATE TABLE users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            );
            CREATE TABLE orders (
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                created_at TEXT
            );
        """,
        "db_seed_sql": """
            INSERT INTO users VALUES (1, 'Алиса');
            INSERT INTO users VALUES (2, 'Боб');
            INSERT INTO orders VALUES (1, 1, 150.0, '2024-01-01');
            INSERT INTO orders VALUES (2, 1, 200.0, '2024-01-15');
            INSERT INTO orders VALUES (3, 2, 50.0,  '2024-02-01');
            INSERT INTO orders VALUES (4, 1, 300.0, '2024-02-10');
            INSERT INTO orders VALUES (5, 2, 120.0, '2024-03-01');
        """,
        "order_matters": True,
        "hints": json.dumps([
            "Используйте COUNT(*) для подсчёта строк.",
            "GROUP BY user_id объединит заказы по пользователю.",
            "ORDER BY order_count DESC — сортировка по убыванию.",
        ]),
    },
    {
        "title": "Имена пользователей с их заказами",
        "description": (
            "Соедините таблицы `users` и `orders` и верните `name` пользователя "
            "и `amount` каждого заказа. Включайте только тех пользователей, "
            "у которых есть хотя бы один заказ."
        ),
        "difficulty": "medium",
        "topic": "JOIN",
        "order_num": 4,
        "reference_sql": (
            "SELECT users.name, orders.amount "
            "FROM users "
            "JOIN orders ON users.id = orders.user_id"
        ),
        "db_schema_sql": """
            CREATE TABLE users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            );
            CREATE TABLE orders (
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                amount REAL NOT NULL
            );
        """,
        "db_seed_sql": """
            INSERT INTO users VALUES (1, 'Алиса');
            INSERT INTO users VALUES (2, 'Боб');
            INSERT INTO users VALUES (3, 'Карл');
            INSERT INTO orders VALUES (1, 1, 150.0);
            INSERT INTO orders VALUES (2, 1, 200.0);
            INSERT INTO orders VALUES (3, 2, 50.0);
        """,
        "order_matters": False,
        "hints": json.dumps([
            "Используйте INNER JOIN (или просто JOIN).",
            "Условие соединения: users.id = orders.user_id.",
        ]),
    },
    {
        "title": "Пользователи без заказов",
        "description": (
            "Найдите имена пользователей, у которых **нет ни одного заказа**. "
            "Верните только столбец `name`."
        ),
        "difficulty": "hard",
        "topic": "JOIN",
        "order_num": 5,
        "reference_sql": (
            "SELECT users.name "
            "FROM users "
            "LEFT JOIN orders ON users.id = orders.user_id "
            "WHERE orders.id IS NULL"
        ),
        "db_schema_sql": """
            CREATE TABLE users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            );
            CREATE TABLE orders (
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                amount REAL NOT NULL
            );
        """,
        "db_seed_sql": """
            INSERT INTO users VALUES (1, 'Алиса');
            INSERT INTO users VALUES (2, 'Боб');
            INSERT INTO users VALUES (3, 'Карл');
            INSERT INTO orders VALUES (1, 1, 150.0);
            INSERT INTO orders VALUES (2, 2, 50.0);
        """,
        "order_matters": False,
        "hints": json.dumps([
            "Используйте LEFT JOIN чтобы включить пользователей без заказов.",
            "WHERE orders.id IS NULL отфильтрует только тех, у кого нет заказов.",
        ]),
    },
]
