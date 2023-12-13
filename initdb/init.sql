CREATE TABLE IF NOT EXISTS companies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    domain VARCHAR(255) UNIQUE,
    additional_info TEXT
);
