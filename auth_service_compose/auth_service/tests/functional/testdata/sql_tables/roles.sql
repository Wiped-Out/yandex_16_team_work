CREATE TABLE IF NOT EXISTS "content"."roles" (
    "name" varchar NOT NULL,
    "level" int4 NOT NULL,
    "id" uuid NOT NULL,
    PRIMARY KEY ("id")
);