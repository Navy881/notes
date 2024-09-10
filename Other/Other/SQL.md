# SQL

Группировка записей по статусу за несколько периодов

```sql
SELECT state_type.state,
       COUNT(DISTINCT event_h.id) AS hour_count,
       COUNT(DISTINCT event_d.id) AS day_count,
       COUNT(DISTINCT event_w.id) AS week_count,
       COUNT(DISTINCT event_m.id) AS month_count
FROM (SELECT unnest(enum_range(NULL::sberprime_subscription_events_states))) AS state_type(state)
LEFT JOIN sberprime_subscription_events event_h ON event_h.state = state_type.state AND event_h.created_at > NOW() - '1 hour'::interval
LEFT JOIN sberprime_subscription_events event_d ON event_d.state = state_type.state AND event_d.created_at > NOW() - '1 day'::interval
LEFT JOIN sberprime_subscription_events event_w ON event_w.state = state_type.state AND event_w.created_at > NOW() - '1 week'::interval
LEFT JOIN sberprime_subscription_events event_m ON event_w.state = state_type.state AND event_w.created_at > NOW() - '1 month'::interval
GROUP BY state_type.state;

SELECT state_type.state, COUNT(event.id)
FROM (SELECT unnest(enum_range(NULL::sberprime_subscription_events_states))) AS state_type(state)
LEFT JOIN sberprime_subscription_events event ON event.state = state_type.state AND event.created_at > NOW() - '1 day'::interval
GROUP BY state_type.state;
```

Перечень записей с условиями из другой таблицы

```sql
select distinct asp.name from public.app_subscription_plan asp
    where asp.status = 'active' and asp.next_pay > now()
    and user_id IN
        (
            select distinct asp.user_id from public.app_subscription_plan asp
            where asp.name like 'sberprime.%'
            and asp.status = 'active'
        )
    and asp.name NOT IN
        (
          select ast.name from public.app_subscription_type ast
          where ast.name like 'sberprime.%'
        )
order by asp.name ASC;
```

Количество записей с условиями из другой таблицы

```sql
select count(asp.user_id) from public.app_subscription_plan asp
    where asp.status = 'active' and asp.next_pay > now()
    and user_id IN
        (
            select distinct asp.user_id from public.app_subscription_plan asp
            where asp.name like 'sberprime.%'
            and asp.status = 'active'
        )
    and asp.name NOT IN
        (
          select ast.name from public.app_subscription_type ast
          where ast.name like 'sberprime.%'
        );
```

Перечень планов подписок Звук+Прайм

```sql
SELECT *, pasp.next_pay - pasp.start FROM public.app_subscription_plan as pasp
WHERE pasp.start > '2021-12-01 00:00:00.000000' AND date_part('day', pasp.next_pay - pasp.start) > 1
  AND pasp.name IN ('me.zvuk.prime.trial',
                    'me.zvuk.prime.1month.renewable.199.trial30d',
                    'me.zvuk.prime.1month.renewable.199.no.trial',
                    'google.zvuk.prime.trial',
                    'google.zvuk.prime.1month.renewable.199.trial30d',
                    'google.zvuk.prime.1month.renewable.199.no.trial')
  AND pasp.user_id NOT IN (509087651,
                           509298857,
                           509331970, 
                           178365150, 
                           509622437,
                           496058386);
```

```sql
SELECT * FROM public.app_subscription_plan as asp
WHERE
      lower(asp.options -> 'number_of_free_periods_issued') LIKE '%1%'
  AND asp.user_id IN (
            SELECT DISTINCT asub.user_id FROM public.app_subscription asub
            WHERE
                  (asub.platform = 'apple' OR asub.platform = 'google')
              AND asub.expiration_date > now()
        );

SELECT COUNT(asp.user_id) FROM public.app_subscription_plan as asp
WHERE
      asp.status = 'removed'
  AND (asp.platform = 'apple' OR asp.platform = 'google')
  AND asp.removed >= '2022-03-03 21:59:59'
  AND NOT exist(asp.options, 'number_of_free_periods_issued') AND asp.user_id NOT IN (
            SELECT DISTINCT asub.user_id FROM public.app_subscription asub
            WHERE
                  (asub.platform = 'apple' OR asub.platform = 'google')
              AND asub.expiration_date > now()
              AND asub.status = 'confirmed'
        )

SELECT asp.platform,
       SUM(CASE WHEN lower(asp.options -> 'number_of_free_periods_issued') LIKE '%1%'
           THEN 1 ELSE 0 END) AS issued,
       SUM(CASE WHEN asp.status = 'removed'
                AND asp.removed >= '2022-03-03 21:59:59'
                AND NOT exist(asp.options, 'number_of_free_periods_issued')
           THEN 1 ELSE 0 END) AS not_issued
FROM public.app_subscription_plan AS asp
WHERE (asp.platform = 'google' OR asp.platform = 'apple')
GROUP BY asp.platform

SELECT 'all_issued' as name, COUNT(asp.user_id) AS count FROM public.app_subscription_plan AS asp
WHERE lower(asp.options -> 'number_of_free_periods_issued') LIKE '%1%'
UNION
SELECT 'google_issued' as name, COUNT(asp.user_id) AS count FROM public.app_subscription_plan AS asp
WHERE asp.platform = 'google' AND lower(asp.options -> 'number_of_free_periods_issued') LIKE '%1%'
UNION
SELECT 'apple_issued' as name, COUNT(asp.user_id) AS count FROM public.app_subscription_plan AS asp
WHERE asp.platform = 'apple' AND lower(asp.options -> 'number_of_free_periods_issued') LIKE '%1%'
UNION
SELECT 'all_not_issued' as name, COUNT(asp.user_id) AS count FROM public.app_subscription_plan AS asp
WHERE asp.status = 'removed'
  AND (asp.platform = 'apple' OR asp.platform = 'google')
  AND asp.removed >= '2022-03-03 21:59:59'
  AND NOT exist(asp.options, 'number_of_free_periods_issued')
UNION
SELECT 'google_not_issued' as name, COUNT(asp.user_id) AS count FROM public.app_subscription_plan AS asp
WHERE asp.status = 'removed'
  AND asp.platform = 'google'
  AND asp.removed >= '2022-03-03 21:59:59'
  AND NOT exist(asp.options, 'number_of_free_periods_issued')
UNION
SELECT 'apple_not_issued' as name, COUNT(asp.user_id) AS count FROM public.app_subscription_plan AS asp
WHERE asp.status = 'removed'
  AND asp.platform = 'apple'
  AND asp.removed >= '2022-03-03 21:59:59'
  AND NOT exist(asp.options, 'number_of_free_periods_issued')

SELECT DATE(asp.removed),
       SUM(CASE WHEN lower(asp.options -> 'number_of_free_periods_issued') LIKE '%1%'
           THEN 1 ELSE 0 END) AS all_issued,
       SUM(CASE WHEN lower(asp.options -> 'number_of_free_periods_issued') LIKE '%1%'
                AND asp.platform = 'google'
           THEN 1 ELSE 0 END) AS google_issued,
       SUM(CASE WHEN lower(asp.options -> 'number_of_free_periods_issued') LIKE '%1%'
                AND asp.platform = 'apple'
           THEN 1 ELSE 0 END) AS apple_issued,
       SUM(CASE WHEN asp.status = 'removed'
                AND (asp.platform = 'apple' OR asp.platform = 'google')
                AND NOT exist(asp.options, 'number_of_free_periods_issued')
           THEN 1 ELSE 0 END) AS all_not_issued,
       SUM(CASE WHEN asp.status = 'removed'
                AND asp.platform = 'google'
                AND asp.removed >= '2022-03-03 21:59:59'
                AND NOT exist(asp.options, 'number_of_free_periods_issued')
           THEN 1 ELSE 0 END) AS google_not_issued,
       SUM(CASE WHEN asp.status = 'removed'
                AND asp.platform = 'apple'
                AND asp.removed >= '2022-03-03 21:59:59'
                AND NOT exist(asp.options, 'number_of_free_periods_issued')
           THEN 1 ELSE 0 END) AS apple_not_issued
FROM public.app_subscription_plan AS asp
WHERE asp.removed BETWEEN '2022-03-02 21:59:59' AND now()
GROUP BY DATE(asp.removed)
ORDER BY DATE(asp.removed)

SELECT * FROM app_subscription_plan as asp
INNER JOIN app_subscription AS asub 
ON asp.id = asub.plan_id
WHERE asp.platform IN ('apple', 'google')
AND exist(asp.options, 'number_of_free_periods_issued')
AND asp.status = 'active'
AND asp.next_pay > '2022-03-10 21:59:59';

SELECT * FROM app_subscription_plan as asp
WHERE asp.platform IN ('apple', 'google')
AND NOT exist(asp.options, 'number_of_free_periods_issued')
AND asp.status = 'active'
AND asp.next_pay > '2022-03-10 21:59:59'
AND asp.id NOT IN (
    SELECT DISTINCT asub.plan_id FROM app_subscription asub
    WHERE asub.expiration_date > '2022-03-10 21:59:59'
    AND asub.platform IN ('apple', 'google')
    AND asub.status != 'cancelled'
);
```

```sql
SELECT tp.id, tr.title, art.name, tp.popularity FROM public.track_popularity AS tp
LEFT OUTER JOIN public.track AS tr ON tp.id = tr.id
LEFT OUTER JOIN artist AS art on art.id = (
    SELECT tart.artist_id FROM tartist AS tart
    WHERE tart.track_id = tp.id
    LIMIT 1)
WHERE tp.popularity >= 2.2
ORDER BY tp.popularity DESC;
```

### Создание БД

```sql
CREATE DATABASE sctgbot;

Подключиться к созданной БД
\c sctgbot;
```

### Создание таблицы в БД

```sql
CREATE TABLE search_markers (
    id SERIAL PRIMARY KEY,
    created_at timestamp NOT NULL DEFAULT NOW(),
    name varchar(255) NOT NULL,
    name_ts tsvector,
    content_id int NOT NULL,
    content_type varchar(255) NOT NULL,
    expiration_at timestamp NOT NULL,
    position integer
);

CREATE TABLE sc_auth_token(
    id SERIAL PRIMARY KEY,
		created_at timestamp NOT NULL DEFAULT NOW(),
		updated_at timestamp NOT NULL DEFAULT NOW(),
    tg_user_id int NOT NULL,
		refresh_token varchar(255) NOT NULL,
		auth_token varchar(1000) NOT NULL
);

CREATE TABLE nalogru_registration(
    id SERIAL PRIMARY KEY,
		created_at timestamp NOT NULL DEFAULT NOW(),
		updated_at timestamp NOT NULL DEFAULT NOW(),
    tg_user_id int NOT NULL,
		is_registered bool NOT NULL DEFAULT False
);

CREATE TABLE sc_events(
    id SERIAL PRIMARY KEY,
		created_at timestamp NOT NULL DEFAULT NOW(),
		updated_at timestamp NOT NULL DEFAULT NOW(),
    tg_user_id int NOT NULL,
		event_id int NOT NULL,
		name varchar(255) NOT NULL
);
```

### Обновление таблицы в БД

```sql
ALTER TABLE users ADD COLUMN updated_at TIMESTAMP without time zone;
```

### Удаление всех таблиц в БД

```sql
drop schema public cascade;
create schema public;
```

### Добавление в таблицу

```sql
INSERT INTO transactions_categories VALUES (2, '2024-04-18T23:11:22', '2024-04-18T23:11:22', 'Продукты', 0, 'Продукты');

INSERT INTO events VALUES (1, '2023-05-03T12:14:22', '2023-05-03T12:14:22', 'Событие 1');
```

### Обновление записи

```sql
UPDATE events SET name = 'Новое имя события' WHERE id = 1;
```

### Удаление записи

```sql
DELETE FROM users WHERE email = 'cudriahca@mail.ru' RETURNING *;
```

### Транзакция

```sql
BEGIN;
INSERT INTO events VALUES (10, '2023-05-03T12:14:22', '2023-05-03T12:14:22', 'Событие 10');
INSERT INTO transactions_categories VALUES (2, '2023-05-03T12:14:22', '2023-05-03T12:14:22', 'Категория 2', 0);
INSERT INTO events VALUES (11, '2023-05-03T12:14:22', '2023-05-03T12:14:22', 'Событие 11');
INSERT INTO events VALUES (12, '2023-05-03T12:14:22', '2023-05-03T12:14:22', 'Событие 12');
INSERT INTO events VALUES (13, '2023-05-03T12:14:22', '2023-05-03T12:14:22', 'Событие 13');
UPDATE events SET name = 'Новое имя события 12' WHERE id = 11;
UPDATE events SET name = 'Новое имя события 12' WHERE id = 12;
UPDATE events SET name = 'Новое имя события 12' WHERE id = 13;
COMMIT;

BEGIN;
INSERT INTO transactions_categories VALUES (1, '2023-05-03T12:14:22', '2023-05-03T12:14:22', 'Категория 1', 0);
INSERT INTO events VALUES (1, '2023-05-03T12:14:22', '2023-05-03T12:14:22', 'Событие 1');
COMMIT;
```

### Количество записей для каждого значения поля

```sql
SELECT l.type, COUNT(*) as count
FROM public.tlyrics AS l
GROUP BY l.type;
```

### Список баз

```sql
\l;
```

### Смена базы

```sql
\connect DBNAME;
```

### Список таблиц базы

```sql
\dt;
```

### Описание таблицы

```sql
\d TABLENAME;
```

### Удалить все зависи из таблицы

```sql
TRUNCATE table_name;
```