SELECT name, year FROM album
WHERE year = 2018;

SELECT name, length FROM track
WHERE length = (SELECT max(length) FROM track);

SELECT name, length FROM track
WHERE length >= 3.5;

SELECT name FROM collection
WHERE year >= 2018 AND YEAR <= 2020;

SELECT name FROM musician
WHERE name NOT LIKE '% %';

SELECT name FROM track
WHERE name LIKE '%Мой%';