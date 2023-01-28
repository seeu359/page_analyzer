DROP TABLE IF EXISTS urls;
CREATE TABLE urls (
    id SERIAL PRIMARY KEY ,
    name VARCHAR(200) UNIQUE,
    created_at DATE
);
