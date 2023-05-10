INSERT INTO musician(name)
VALUES ('Rammstein'), 
('AC-DC'), 
('Ария'), 
('NIRVANA'), 
('Дима Билан'), 
('Михаил Круг'), 
('Сергей Наговицын'), 
('SEREBRO');

INSERT INTO genre(name)
VALUES ('Альтернативный Рок'), 
('Хеви-Метал'), 
('Поп-музыка'), 
('Шансон'), 
('Панк-Рок');

INSERT INTO album(name, year)
VALUES ('Live Aus Berlin', 1999), 
('Крещение огнем', 2003), 
('High Voltage', 1975), 
('Разбитая судьба', 2018), 
('Nevermind', 1991), 
('Я ночной хулиган', 2003), 
('Владимирский централ', 1999), 
('Mama Lover', 2012);

INSERT INTO track(name, length, album_id)
VALUES ('Du Hast', 2.7, 1), 
('Links 234', 3.6, 1), 
('Back in Black', 3.99, 3),
('Пробил час', 2.05, 2), 
('Колизей', 2.71, 2), 
('Smells like teen spirit', 3.1, 5),
('Мой мир', 4.2, 6), 
('Never Let You Go', 3.36, 6), 
('Исповедь', 2.85, 7),
('Магадан', 3.75, 7), 
('Дори Дори', 2.78, 4), 
('Приговор', 1.8, 4),
('Столичная', 3.0, 4), 
('Скажи, не молчи', 2.45, 8), 
('Между нами любовь', 3.99, 8);

INSERT INTO collection(name, year)
VALUES ('Black Metal', 2010),
('Русский Шансон', 2015),
('Популярная', 2019),
('Немецкая музыка', 2013),
('Рокеры из Штатов',  2008);

INSERT INTO collection_track(collection_id, track_id)
VALUES (4, 1), (4, 2), (5, 3), (1, 4), (1, 5), (5, 6), (3, 7), (3, 8), (2, 9), (2, 10),
(2, 11), (2, 12), (2, 13), (3, 14), (3, 15);

INSERT INTO genre_musician(genre_id, musician_id)
VALUES (1, 1), (2, 2), (2, 3), (5, 4), (3, 5), (4, 6), (4, 7), (3, 8);

INSERT INTO musician_album(musician_id, album_id)
VALUES (1, 1), (2, 3), (3, 2), (4, 5), (5, 6), (6, 7), (7, 4), (8, 8);