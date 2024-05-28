CREATE TABLE public."user"
(
    id         serial PRIMARY KEY,
    email      varchar(255) NOT NULL,
    "password" varchar(255) NOT null,
    username   varchar(255) NOT NULL
);
