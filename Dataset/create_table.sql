CREATE TABLE IF NOT EXISTS users(
    handle text NOT NULL,
    firstName text,
    lastName text,
    country text,
    rank text,
    rating bigint,
    passwd text,
    CONSTRAINT user_key  PRIMARY KEY (handle)
);


-- \copy users from 'Codeforces/Dataset/users.csv' delimiter ',' csv header;