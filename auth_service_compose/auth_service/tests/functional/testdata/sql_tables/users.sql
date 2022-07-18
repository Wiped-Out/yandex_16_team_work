CREATE TABLE IF NOT EXISTS "content"."users" (
    "login" varchar NOT NULL UNIQUE,
    "password" varchar NOT NULL,
    "email" varchar NOT NULL UNIQUE,
    "id" uuid NOT NULL,
    PRIMARY KEY ("id")
);