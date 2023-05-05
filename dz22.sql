CREATE TABLE IF NOT EXISTS names (
	id serial PRIMARY KEY,
	name VARCHAR(30)
);

CREATE TABLE IF NOT EXISTS department (
	id serial PRIMARY KEY,
	name VARCHAR(30)
);

CREATE TABLE IF NOT EXISTS position (
	id serial PRIMARY KEY,
	name VARCHAR(30)
);

CREATE TABLE IF NOT EXISTS employee (
	id serial PRIMARY KEY,
	name INTEGER,
	position INTEGER,
	department INTEGER,
	boss_id INTEGER,
	FOREIGN KEY (department) REFERENCES department(id),
	FOREIGN KEY (boss_id) REFERENCES names(id),
	FOREIGN KEY (position) REFERENCES position(id),
	FOREIGN KEY (name) REFERENCES names (id)
);