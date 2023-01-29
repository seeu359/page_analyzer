DROP TABLE IF EXISTS urls;
DROP TABLE IF EXISTS url_checks;

CREATE TABLE urls (
    id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(200) UNIQUE,
    created_at DATE
);

CREATE TABLE url_checks (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    url_id BIGINT references urls (id),
    status_code INTEGER,
    h1 VARCHAR(300),
    title VARCHAR(250),
    description VARCHAR(250),
    created_at DATE
);

