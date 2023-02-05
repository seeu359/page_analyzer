DROP TABLE IF EXISTS url_checks;
DROP TABLE IF EXISTS all_sites;
DROP TABLE IF EXISTS urls;

CREATE TABLE urls (
    id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(200) UNIQUE,
    created_at TIMESTAMP
);

CREATE TABLE url_checks (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    url_id BIGINT references urls (id),
    status_code INTEGER,
    h1 VARCHAR,
    title VARCHAR,
    description VARCHAR,
    created_at TIMESTAMP
);


CREATE TABLE all_sites (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    url_id BIGINT references urls (id),
    CREATED_AT TIMESTAMP,
    status_code INTEGER
);
