--
-- PostgreSQL database dump
--

-- Dumped from database version 16.4
-- Dumped by pg_dump version 16.4

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

--
-- Name: actors; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.actors (
    actor_id integer NOT NULL,
    actor_name character varying(255)
);


ALTER TABLE public.actors OWNER TO postgres;

--
-- Name: cast; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."cast" (
    cast_id integer NOT NULL,
    movie_id character varying,
    actor_id integer
);


ALTER TABLE public."cast" OWNER TO postgres;

--
-- Name: directors; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.directors (
    director_id integer NOT NULL,
    director_name character varying
);


ALTER TABLE public.directors OWNER TO postgres;

--
-- Name: funny_words; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.funny_words (
    id integer NOT NULL,
    word character varying(255) NOT NULL
);


ALTER TABLE public.funny_words OWNER TO postgres;

--
-- Name: funny_words_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.funny_words_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.funny_words_id_seq OWNER TO postgres;

--
-- Name: funny_words_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.funny_words_id_seq OWNED BY public.funny_words.id;


--
-- Name: movie_and_tv; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.movie_and_tv (
    show_id character varying(15) NOT NULL,
    from_service "char",
    type character varying(10),
    title character varying(255),
    country character varying(255),
    release_year integer,
    rating character varying(20),
    duration character varying(50),
    genre character varying(255),
    description character varying(5000)
);


ALTER TABLE public.movie_and_tv OWNER TO postgres;

--
-- Name: movie_directors; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.movie_directors (
    entry_id integer NOT NULL,
    movie_id character varying(25),
    director_id integer
);


ALTER TABLE public.movie_directors OWNER TO postgres;

--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    username character varying(50) NOT NULL,
    salt text NOT NULL,
    password_hash text NOT NULL
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_user_id_seq OWNER TO postgres;

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;


--
-- Name: funny_words id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.funny_words ALTER COLUMN id SET DEFAULT nextval('public.funny_words_id_seq'::regclass);


--
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- Name: actors actors_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.actors
    ADD CONSTRAINT actors_pkey PRIMARY KEY (actor_id);


--
-- Name: cast cast_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."cast"
    ADD CONSTRAINT cast_pkey PRIMARY KEY (cast_id);


--
-- Name: directors directors_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.directors
    ADD CONSTRAINT directors_pkey PRIMARY KEY (director_id);


--
-- Name: funny_words funny_words_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.funny_words
    ADD CONSTRAINT funny_words_pkey PRIMARY KEY (id);


--
-- Name: movie_and_tv movie_and_tv_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.movie_and_tv
    ADD CONSTRAINT movie_and_tv_pkey PRIMARY KEY (show_id);


--
-- Name: movie_directors movie_directors_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.movie_directors
    ADD CONSTRAINT movie_directors_pkey PRIMARY KEY (entry_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- PostgreSQL database dump complete
--

