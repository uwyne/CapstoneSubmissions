--
-- PostgreSQL database dump
--

-- Dumped from database version 12.3
-- Dumped by pg_dump version 12.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

-- Role: uwyne
DROP ROLE IF EXISTS uwyne;

CREATE ROLE uwyne WITH LOGIN SUPERUSER INHERIT CREATEDB CREATEROLE NOREPLICATION PASSWORD 'password1';

--
-- Name: actors; Type: TABLE; Schema: public; Owner: uwyne
--

CREATE TABLE public.actors (
    id integer NOT NULL,
    name character varying NOT NULL,
    age integer NOT NULL,
    gender character varying NOT NULL,
    movie_id integer NOT NULL
);


ALTER TABLE public.actors OWNER TO uwyne;

--
-- Name: actors_id_seq; Type: SEQUENCE; Schema: public; Owner: uwyne
--

CREATE SEQUENCE public.actors_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.actors_id_seq OWNER TO uwyne;

--
-- Name: actors_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: uwyne
--

ALTER SEQUENCE public.actors_id_seq OWNED BY public.actors.id;


--
-- Name: movies; Type: TABLE; Schema: public; Owner: uwyne
--

CREATE TABLE public.movies (
    id integer NOT NULL,
    title character varying NOT NULL,
    release_date timestamp without time zone NOT NULL
);


ALTER TABLE public.movies OWNER TO uwyne;

--
-- Name: movies_id_seq; Type: SEQUENCE; Schema: public; Owner: uwyne
--

CREATE SEQUENCE public.movies_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.movies_id_seq OWNER TO uwyne;

--
-- Name: movies_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: uwyne
--

ALTER SEQUENCE public.movies_id_seq OWNED BY public.movies.id;


--
-- Name: actors id; Type: DEFAULT; Schema: public; Owner: uwyne
--

ALTER TABLE ONLY public.actors ALTER COLUMN id SET DEFAULT nextval('public.actors_id_seq'::regclass);


--
-- Name: movies id; Type: DEFAULT; Schema: public; Owner: uwyne
--

ALTER TABLE ONLY public.movies ALTER COLUMN id SET DEFAULT nextval('public.movies_id_seq'::regclass);


--
-- Data for Name: actors; Type: TABLE DATA; Schema: public; Owner: uwyne
--

COPY public.actors (id, name, age, gender, movie_id) FROM stdin;
1	Tom Cruise	60	M	1
2	Benedict Cumberbatch	46	M	2
3	Letitia Wright	29 F	3
4	Chris Hemsworth	39	M	4
\.


--
-- Data for Name: movies; Type: TABLE DATA; Schema: public; Owner: uwyne
--

COPY public.movies (id, title, release_date) FROM stdin;
1	Top Gun: Maverick	2022-04-28 00:00:00
2	Doctor Strange in the Multiverse of Madness	2022-05-02 00:00:00
3	Black Panther: Wakanda Forever	2022-10-26 00:00:00
4	Thor: Love and Thunder	2022-06-23 00:00:00
\.


--
-- Name: actors_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uwyne
--

SELECT pg_catalog.setval('public.actors_id_seq', 10, true);


--
-- Name: movies_id_seq; Type: SEQUENCE SET; Schema: public; Owner: uwyne
--

SELECT pg_catalog.setval('public.movies_id_seq', 15, true);


--
-- Name: actors actors_pkey; Type: CONSTRAINT; Schema: public; Owner: uwyne
--

ALTER TABLE ONLY public.actors
    ADD CONSTRAINT actors_pkey PRIMARY KEY (id);


--
-- Name: movies movies_pkey; Type: CONSTRAINT; Schema: public; Owner: uwyne
--

ALTER TABLE ONLY public.movies
    ADD CONSTRAINT movies_pkey PRIMARY KEY (id);


--
-- Name: actors actors_movie_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: uwyne
--

ALTER TABLE ONLY public.actors
    ADD CONSTRAINT actors_movie_id_fkey FOREIGN KEY (movie_id) REFERENCES public.movies(id);


--
-- PostgreSQL database dump complete
--
