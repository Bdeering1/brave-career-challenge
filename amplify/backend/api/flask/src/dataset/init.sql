CREATE TABLE IF NOT EXISTS public.site
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    url_root text COLLATE pg_catalog."default" NOT NULL,
    name text COLLATE pg_catalog."default" NOT NULL,
    description text COLLATE pg_catalog."default" NOT NULL,
    offerings text[] COLLATE pg_catalog."default" NOT NULL,
    prompt text COLLATE pg_catalog."default",
    options text[] COLLATE pg_catalog."default",
    CONSTRAINT site_pkey PRIMARY KEY (id)
)
TABLESPACE pg_default;
