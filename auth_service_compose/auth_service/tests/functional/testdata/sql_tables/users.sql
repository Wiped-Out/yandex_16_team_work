CREATE TABLE IF NOT EXISTS "content"."users" (
    "login" varchar NOT NULL,
    "password" varchar NOT NULL,
    "email" varchar NOT NULL,
    "id" uuid NOT NULL,
    PRIMARY KEY ("id")
);