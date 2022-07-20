CREATE TABLE "content"."user_roles"
(
    "user_id" uuid NOT NULL,
    "role_id" uuid NOT NULL,
    CONSTRAINT "user_roles_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "content"."users" ("id")
);