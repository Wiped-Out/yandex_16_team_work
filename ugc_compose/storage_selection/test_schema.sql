CREATE SCHEMA IF NOT EXISTS test_data;


CREATE TABLE IF NOT EXISTS test_data.film_like (
    id uuid PRIMARY KEY,
    user_id uuid NOT NULL,
    film_id uuid NOT NULL,
    rating INT NOT NULL
);

CREATE TABLE IF NOT EXISTS test_data.film_bookmark (
    id uuid PRIMARY KEY,
    user_id uuid NOT NULL,
    film_id uuid NOT NULL
);

CREATE TABLE IF NOT EXISTS test_data.user_review (
    id uuid PRIMARY KEY,
    user_id uuid NOT NULL,
    film_id uuid NOT NULL,
    text TEXT,
    created_at timestamp with time zone
);

CREATE INDEX film_like_index ON test_data.film_like (user_id, film_id);
CREATE INDEX film_bookmark_index ON test_data.film_bookmark (user_id, film_id);
CREATE INDEX user_review_index ON test_data.user_review (user_id, film_id);
