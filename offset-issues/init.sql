create table news
(
id serial not null primary key,
title text,
a text,
b text,
c integer
);

-- populate the table
INSERT INTO news (title, a, b, c)
SELECT 
    substring(md5(random()::text), 1, 10) as title,
    substring(md5(random()::text), 1, 10) as a,
    substring(md5(random()::text), 1, 10) as b,
    (random() * 1000)::integer as c
FROM generate_series(1, 1000000);