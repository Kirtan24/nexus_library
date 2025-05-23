PGDMP  ;    )        
        }            NexusLibrary    17.0    17.0 z    �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                           false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                           false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                           false            �           1262    18243    NexusLibrary    DATABASE     �   CREATE DATABASE "NexusLibrary" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'English_India.1252';
    DROP DATABASE "NexusLibrary";
                     postgres    false            �            1259    18578 
   audiobooks    TABLE     �   CREATE TABLE public.audiobooks (
    item_id integer NOT NULL,
    narrator character varying(100),
    duration_minutes integer,
    description text,
    publisher character varying(100)
);
    DROP TABLE public.audiobooks;
       public         heap r       postgres    false            �            1259    18324    authors    TABLE     �   CREATE TABLE public.authors (
    author_id integer NOT NULL,
    name character varying(100) NOT NULL,
    bio text,
    nationality character varying(100),
    genres text[]
);
    DROP TABLE public.authors;
       public         heap r       postgres    false            �            1259    18323    authors_author_id_seq    SEQUENCE     �   CREATE SEQUENCE public.authors_author_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 ,   DROP SEQUENCE public.authors_author_id_seq;
       public               postgres    false    226            �           0    0    authors_author_id_seq    SEQUENCE OWNED BY     O   ALTER SEQUENCE public.authors_author_id_seq OWNED BY public.authors.author_id;
          public               postgres    false    225            �            1259    18685    borrow_records    TABLE        CREATE TABLE public.borrow_records (
    record_id integer NOT NULL,
    user_id integer NOT NULL,
    item_id integer NOT NULL,
    borrow_date date NOT NULL,
    due_date date NOT NULL,
    return_date date,
    fine_amount numeric(10,2) DEFAULT 0.00
);
 "   DROP TABLE public.borrow_records;
       public         heap r       postgres    false            �            1259    18684    borrow_records_record_id_seq    SEQUENCE     �   CREATE SEQUENCE public.borrow_records_record_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 3   DROP SEQUENCE public.borrow_records_record_id_seq;
       public               postgres    false    241            �           0    0    borrow_records_record_id_seq    SEQUENCE OWNED BY     ]   ALTER SEQUENCE public.borrow_records_record_id_seq OWNED BY public.borrow_records.record_id;
          public               postgres    false    240            �            1259    18554    ebooks    TABLE     �   CREATE TABLE public.ebooks (
    item_id integer NOT NULL,
    cover_image_url character varying(255),
    description text,
    publisher_url character varying(255)
);
    DROP TABLE public.ebooks;
       public         heap r       postgres    false            �            1259    18704    fines    TABLE     ;  CREATE TABLE public.fines (
    fine_id integer NOT NULL,
    user_id integer NOT NULL,
    borrow_record_id integer NOT NULL,
    amount numeric(10,2) NOT NULL,
    status character varying(20) DEFAULT 'unpaid'::character varying NOT NULL,
    issued_date date DEFAULT CURRENT_DATE NOT NULL,
    paid_date date
);
    DROP TABLE public.fines;
       public         heap r       postgres    false            �            1259    18703    fines_fine_id_seq    SEQUENCE     �   CREATE SEQUENCE public.fines_fine_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.fines_fine_id_seq;
       public               postgres    false    243            �           0    0    fines_fine_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.fines_fine_id_seq OWNED BY public.fines.fine_id;
          public               postgres    false    242            �            1259    18664    item_observers    TABLE     C  CREATE TABLE public.item_observers (
    observer_id integer NOT NULL,
    user_id integer NOT NULL,
    item_id integer NOT NULL,
    status character varying(20) DEFAULT 'active'::character varying NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    priority integer DEFAULT 0
);
 "   DROP TABLE public.item_observers;
       public         heap r       postgres    false            �            1259    18663    item_observers_observer_id_seq    SEQUENCE     �   CREATE SEQUENCE public.item_observers_observer_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 5   DROP SEQUENCE public.item_observers_observer_id_seq;
       public               postgres    false    239            �           0    0    item_observers_observer_id_seq    SEQUENCE OWNED BY     a   ALTER SEQUENCE public.item_observers_observer_id_seq OWNED BY public.item_observers.observer_id;
          public               postgres    false    238            �            1259    18629    items    TABLE     K  CREATE TABLE public.items (
    item_id integer NOT NULL,
    title character varying(255) NOT NULL,
    author_id integer NOT NULL,
    genre character varying(100),
    publication_year integer,
    availability_status character varying(50) DEFAULT 'Available'::character varying,
    item_type character varying(50) NOT NULL
);
    DROP TABLE public.items;
       public         heap r       postgres    false            �            1259    18628    items_item_id_seq    SEQUENCE     �   CREATE SEQUENCE public.items_item_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.items_item_id_seq;
       public               postgres    false    235            �           0    0    items_item_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.items_item_id_seq OWNED BY public.items.item_id;
          public               postgres    false    234            �            1259    18643    notifications    TABLE     x  CREATE TABLE public.notifications (
    notification_id integer NOT NULL,
    user_id integer NOT NULL,
    item_id integer NOT NULL,
    notification_type character varying(50) NOT NULL,
    message text NOT NULL,
    status character varying(20) DEFAULT 'pending'::character varying NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);
 !   DROP TABLE public.notifications;
       public         heap r       postgres    false            �            1259    18642 !   notifications_notification_id_seq    SEQUENCE     �   CREATE SEQUENCE public.notifications_notification_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 8   DROP SEQUENCE public.notifications_notification_id_seq;
       public               postgres    false    237            �           0    0 !   notifications_notification_id_seq    SEQUENCE OWNED BY     g   ALTER SEQUENCE public.notifications_notification_id_seq OWNED BY public.notifications.notification_id;
          public               postgres    false    236            �            1259    18296    permissions    TABLE     �   CREATE TABLE public.permissions (
    permission_id integer NOT NULL,
    permission_name character varying(100) NOT NULL,
    description text,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);
    DROP TABLE public.permissions;
       public         heap r       postgres    false            �            1259    18295    permissions_permission_id_seq    SEQUENCE     �   CREATE SEQUENCE public.permissions_permission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 4   DROP SEQUENCE public.permissions_permission_id_seq;
       public               postgres    false    223            �           0    0    permissions_permission_id_seq    SEQUENCE OWNED BY     _   ALTER SEQUENCE public.permissions_permission_id_seq OWNED BY public.permissions.permission_id;
          public               postgres    false    222            �            1259    18618    printed_books    TABLE     �   CREATE TABLE public.printed_books (
    item_id integer NOT NULL,
    isbn character varying(20),
    shelf_location character varying(50),
    total_copies integer DEFAULT 1 NOT NULL,
    available_copies integer DEFAULT 1 NOT NULL
);
 !   DROP TABLE public.printed_books;
       public         heap r       postgres    false            �            1259    18617    printed_books_book_id_seq    SEQUENCE     �   CREATE SEQUENCE public.printed_books_book_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 0   DROP SEQUENCE public.printed_books_book_id_seq;
       public               postgres    false    233            �           0    0    printed_books_book_id_seq    SEQUENCE OWNED BY     W   ALTER SEQUENCE public.printed_books_book_id_seq OWNED BY public.printed_books.item_id;
          public               postgres    false    232            �            1259    18566    research_papers    TABLE     �   CREATE TABLE public.research_papers (
    item_id integer NOT NULL,
    abstract text,
    journal_name character varying(255),
    doi character varying(100),
    conference_name character varying(255)
);
 #   DROP TABLE public.research_papers;
       public         heap r       postgres    false            �            1259    18370    reservations    TABLE     �  CREATE TABLE public.reservations (
    reservation_id integer NOT NULL,
    user_id integer,
    book_id integer,
    reservation_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    status character varying(20) DEFAULT 'Pending'::character varying,
    CONSTRAINT reservations_status_check CHECK (((status)::text = ANY ((ARRAY['Pending'::character varying, 'Completed'::character varying, 'Cancelled'::character varying])::text[])))
);
     DROP TABLE public.reservations;
       public         heap r       postgres    false            �            1259    18369    reservations_reservation_id_seq    SEQUENCE     �   CREATE SEQUENCE public.reservations_reservation_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 6   DROP SEQUENCE public.reservations_reservation_id_seq;
       public               postgres    false    228            �           0    0    reservations_reservation_id_seq    SEQUENCE OWNED BY     c   ALTER SEQUENCE public.reservations_reservation_id_seq OWNED BY public.reservations.reservation_id;
          public               postgres    false    227            �            1259    18307    role_permissions    TABLE     �   CREATE TABLE public.role_permissions (
    role_id integer NOT NULL,
    permission_id integer NOT NULL,
    granted_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);
 $   DROP TABLE public.role_permissions;
       public         heap r       postgres    false            �            1259    18263    roles    TABLE     �   CREATE TABLE public.roles (
    role_id integer NOT NULL,
    role_name character varying(50) NOT NULL,
    description text,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);
    DROP TABLE public.roles;
       public         heap r       postgres    false            �            1259    18262    roles_role_id_seq    SEQUENCE     �   CREATE SEQUENCE public.roles_role_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.roles_role_id_seq;
       public               postgres    false    220            �           0    0    roles_role_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.roles_role_id_seq OWNED BY public.roles.role_id;
          public               postgres    false    219            �            1259    18274 
   user_roles    TABLE     �   CREATE TABLE public.user_roles (
    user_id integer NOT NULL,
    role_id integer NOT NULL,
    assigned_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    assigned_by integer
);
    DROP TABLE public.user_roles;
       public         heap r       postgres    false            �            1259    18245    users    TABLE     �  CREATE TABLE public.users (
    user_id integer NOT NULL,
    username character varying(50) NOT NULL,
    email character varying(100) NOT NULL,
    password_hash character varying(255) NOT NULL,
    phone_number character varying(20),
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    last_login timestamp with time zone,
    account_status character varying(20) DEFAULT 'active'::character varying,
    name character varying(50) NOT NULL,
    CONSTRAINT users_account_status_check CHECK (((account_status)::text = ANY ((ARRAY['active'::character varying, 'suspended'::character varying, 'inactive'::character varying])::text[])))
);
    DROP TABLE public.users;
       public         heap r       postgres    false            �            1259    18244    users_user_id_seq    SEQUENCE     �   CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.users_user_id_seq;
       public               postgres    false    218            �           0    0    users_user_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;
          public               postgres    false    217            �           2604    18327    authors author_id    DEFAULT     v   ALTER TABLE ONLY public.authors ALTER COLUMN author_id SET DEFAULT nextval('public.authors_author_id_seq'::regclass);
 @   ALTER TABLE public.authors ALTER COLUMN author_id DROP DEFAULT;
       public               postgres    false    225    226    226            �           2604    18688    borrow_records record_id    DEFAULT     �   ALTER TABLE ONLY public.borrow_records ALTER COLUMN record_id SET DEFAULT nextval('public.borrow_records_record_id_seq'::regclass);
 G   ALTER TABLE public.borrow_records ALTER COLUMN record_id DROP DEFAULT;
       public               postgres    false    240    241    241            �           2604    18707    fines fine_id    DEFAULT     n   ALTER TABLE ONLY public.fines ALTER COLUMN fine_id SET DEFAULT nextval('public.fines_fine_id_seq'::regclass);
 <   ALTER TABLE public.fines ALTER COLUMN fine_id DROP DEFAULT;
       public               postgres    false    243    242    243            �           2604    18667    item_observers observer_id    DEFAULT     �   ALTER TABLE ONLY public.item_observers ALTER COLUMN observer_id SET DEFAULT nextval('public.item_observers_observer_id_seq'::regclass);
 I   ALTER TABLE public.item_observers ALTER COLUMN observer_id DROP DEFAULT;
       public               postgres    false    238    239    239            �           2604    18632    items item_id    DEFAULT     n   ALTER TABLE ONLY public.items ALTER COLUMN item_id SET DEFAULT nextval('public.items_item_id_seq'::regclass);
 <   ALTER TABLE public.items ALTER COLUMN item_id DROP DEFAULT;
       public               postgres    false    235    234    235            �           2604    18646    notifications notification_id    DEFAULT     �   ALTER TABLE ONLY public.notifications ALTER COLUMN notification_id SET DEFAULT nextval('public.notifications_notification_id_seq'::regclass);
 L   ALTER TABLE public.notifications ALTER COLUMN notification_id DROP DEFAULT;
       public               postgres    false    236    237    237            �           2604    18299    permissions permission_id    DEFAULT     �   ALTER TABLE ONLY public.permissions ALTER COLUMN permission_id SET DEFAULT nextval('public.permissions_permission_id_seq'::regclass);
 H   ALTER TABLE public.permissions ALTER COLUMN permission_id DROP DEFAULT;
       public               postgres    false    222    223    223            �           2604    18621    printed_books item_id    DEFAULT     ~   ALTER TABLE ONLY public.printed_books ALTER COLUMN item_id SET DEFAULT nextval('public.printed_books_book_id_seq'::regclass);
 D   ALTER TABLE public.printed_books ALTER COLUMN item_id DROP DEFAULT;
       public               postgres    false    233    232    233            �           2604    18373    reservations reservation_id    DEFAULT     �   ALTER TABLE ONLY public.reservations ALTER COLUMN reservation_id SET DEFAULT nextval('public.reservations_reservation_id_seq'::regclass);
 J   ALTER TABLE public.reservations ALTER COLUMN reservation_id DROP DEFAULT;
       public               postgres    false    228    227    228            �           2604    18266    roles role_id    DEFAULT     n   ALTER TABLE ONLY public.roles ALTER COLUMN role_id SET DEFAULT nextval('public.roles_role_id_seq'::regclass);
 <   ALTER TABLE public.roles ALTER COLUMN role_id DROP DEFAULT;
       public               postgres    false    220    219    220            �           2604    18248    users user_id    DEFAULT     n   ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);
 <   ALTER TABLE public.users ALTER COLUMN user_id DROP DEFAULT;
       public               postgres    false    218    217    218            �          0    18578 
   audiobooks 
   TABLE DATA           a   COPY public.audiobooks (item_id, narrator, duration_minutes, description, publisher) FROM stdin;
    public               postgres    false    231   �       �          0    18324    authors 
   TABLE DATA           L   COPY public.authors (author_id, name, bio, nationality, genres) FROM stdin;
    public               postgres    false    226   Ş       �          0    18685    borrow_records 
   TABLE DATA           v   COPY public.borrow_records (record_id, user_id, item_id, borrow_date, due_date, return_date, fine_amount) FROM stdin;
    public               postgres    false    241   ^�       �          0    18554    ebooks 
   TABLE DATA           V   COPY public.ebooks (item_id, cover_image_url, description, publisher_url) FROM stdin;
    public               postgres    false    229   �       �          0    18704    fines 
   TABLE DATA           k   COPY public.fines (fine_id, user_id, borrow_record_id, amount, status, issued_date, paid_date) FROM stdin;
    public               postgres    false    243   z�       �          0    18664    item_observers 
   TABLE DATA           e   COPY public.item_observers (observer_id, user_id, item_id, status, created_at, priority) FROM stdin;
    public               postgres    false    239   ��       �          0    18629    items 
   TABLE DATA           s   COPY public.items (item_id, title, author_id, genre, publication_year, availability_status, item_type) FROM stdin;
    public               postgres    false    235   �       �          0    18643    notifications 
   TABLE DATA           z   COPY public.notifications (notification_id, user_id, item_id, notification_type, message, status, created_at) FROM stdin;
    public               postgres    false    237   Y�       �          0    18296    permissions 
   TABLE DATA           ^   COPY public.permissions (permission_id, permission_name, description, created_at) FROM stdin;
    public               postgres    false    223   ��       �          0    18618    printed_books 
   TABLE DATA           f   COPY public.printed_books (item_id, isbn, shelf_location, total_copies, available_copies) FROM stdin;
    public               postgres    false    233   	�       �          0    18566    research_papers 
   TABLE DATA           `   COPY public.research_papers (item_id, abstract, journal_name, doi, conference_name) FROM stdin;
    public               postgres    false    230   P�       �          0    18370    reservations 
   TABLE DATA           b   COPY public.reservations (reservation_id, user_id, book_id, reservation_date, status) FROM stdin;
    public               postgres    false    228   ٩       �          0    18307    role_permissions 
   TABLE DATA           N   COPY public.role_permissions (role_id, permission_id, granted_at) FROM stdin;
    public               postgres    false    224   ��       �          0    18263    roles 
   TABLE DATA           L   COPY public.roles (role_id, role_name, description, created_at) FROM stdin;
    public               postgres    false    220   �       �          0    18274 
   user_roles 
   TABLE DATA           P   COPY public.user_roles (user_id, role_id, assigned_at, assigned_by) FROM stdin;
    public               postgres    false    221   �       �          0    18245    users 
   TABLE DATA           �   COPY public.users (user_id, username, email, password_hash, phone_number, created_at, last_login, account_status, name) FROM stdin;
    public               postgres    false    218   �       �           0    0    authors_author_id_seq    SEQUENCE SET     D   SELECT pg_catalog.setval('public.authors_author_id_seq', 13, true);
          public               postgres    false    225            �           0    0    borrow_records_record_id_seq    SEQUENCE SET     K   SELECT pg_catalog.setval('public.borrow_records_record_id_seq', 30, true);
          public               postgres    false    240            �           0    0    fines_fine_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.fines_fine_id_seq', 1, true);
          public               postgres    false    242            �           0    0    item_observers_observer_id_seq    SEQUENCE SET     M   SELECT pg_catalog.setval('public.item_observers_observer_id_seq', 13, true);
          public               postgres    false    238            �           0    0    items_item_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.items_item_id_seq', 9, true);
          public               postgres    false    234            �           0    0 !   notifications_notification_id_seq    SEQUENCE SET     O   SELECT pg_catalog.setval('public.notifications_notification_id_seq', 8, true);
          public               postgres    false    236            �           0    0    permissions_permission_id_seq    SEQUENCE SET     L   SELECT pg_catalog.setval('public.permissions_permission_id_seq', 15, true);
          public               postgres    false    222            �           0    0    printed_books_book_id_seq    SEQUENCE SET     H   SELECT pg_catalog.setval('public.printed_books_book_id_seq', 1, false);
          public               postgres    false    232            �           0    0    reservations_reservation_id_seq    SEQUENCE SET     N   SELECT pg_catalog.setval('public.reservations_reservation_id_seq', 1, false);
          public               postgres    false    227            �           0    0    roles_role_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.roles_role_id_seq', 6, true);
          public               postgres    false    219            �           0    0    users_user_id_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('public.users_user_id_seq', 15, true);
          public               postgres    false    217            	           2606    18584    audiobooks audiobooks_pkey 
   CONSTRAINT     ]   ALTER TABLE ONLY public.audiobooks
    ADD CONSTRAINT audiobooks_pkey PRIMARY KEY (item_id);
 D   ALTER TABLE ONLY public.audiobooks DROP CONSTRAINT audiobooks_pkey;
       public                 postgres    false    231                        2606    18331    authors authors_pkey 
   CONSTRAINT     Y   ALTER TABLE ONLY public.authors
    ADD CONSTRAINT authors_pkey PRIMARY KEY (author_id);
 >   ALTER TABLE ONLY public.authors DROP CONSTRAINT authors_pkey;
       public                 postgres    false    226                       2606    18692 "   borrow_records borrow_records_pkey 
   CONSTRAINT     g   ALTER TABLE ONLY public.borrow_records
    ADD CONSTRAINT borrow_records_pkey PRIMARY KEY (record_id);
 L   ALTER TABLE ONLY public.borrow_records DROP CONSTRAINT borrow_records_pkey;
       public                 postgres    false    241                       2606    18560    ebooks ebooks_pkey 
   CONSTRAINT     U   ALTER TABLE ONLY public.ebooks
    ADD CONSTRAINT ebooks_pkey PRIMARY KEY (item_id);
 <   ALTER TABLE ONLY public.ebooks DROP CONSTRAINT ebooks_pkey;
       public                 postgres    false    229                       2606    18711    fines fines_pkey 
   CONSTRAINT     S   ALTER TABLE ONLY public.fines
    ADD CONSTRAINT fines_pkey PRIMARY KEY (fine_id);
 :   ALTER TABLE ONLY public.fines DROP CONSTRAINT fines_pkey;
       public                 postgres    false    243                       2606    18671 "   item_observers item_observers_pkey 
   CONSTRAINT     i   ALTER TABLE ONLY public.item_observers
    ADD CONSTRAINT item_observers_pkey PRIMARY KEY (observer_id);
 L   ALTER TABLE ONLY public.item_observers DROP CONSTRAINT item_observers_pkey;
       public                 postgres    false    239                       2606    18673 1   item_observers item_observers_user_id_item_id_key 
   CONSTRAINT     x   ALTER TABLE ONLY public.item_observers
    ADD CONSTRAINT item_observers_user_id_item_id_key UNIQUE (user_id, item_id);
 [   ALTER TABLE ONLY public.item_observers DROP CONSTRAINT item_observers_user_id_item_id_key;
       public                 postgres    false    239    239                       2606    18635    items items_pkey 
   CONSTRAINT     S   ALTER TABLE ONLY public.items
    ADD CONSTRAINT items_pkey PRIMARY KEY (item_id);
 :   ALTER TABLE ONLY public.items DROP CONSTRAINT items_pkey;
       public                 postgres    false    235                       2606    18652     notifications notifications_pkey 
   CONSTRAINT     k   ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_pkey PRIMARY KEY (notification_id);
 J   ALTER TABLE ONLY public.notifications DROP CONSTRAINT notifications_pkey;
       public                 postgres    false    237            �           2606    18306 +   permissions permissions_permission_name_key 
   CONSTRAINT     q   ALTER TABLE ONLY public.permissions
    ADD CONSTRAINT permissions_permission_name_key UNIQUE (permission_name);
 U   ALTER TABLE ONLY public.permissions DROP CONSTRAINT permissions_permission_name_key;
       public                 postgres    false    223            �           2606    18304    permissions permissions_pkey 
   CONSTRAINT     e   ALTER TABLE ONLY public.permissions
    ADD CONSTRAINT permissions_pkey PRIMARY KEY (permission_id);
 F   ALTER TABLE ONLY public.permissions DROP CONSTRAINT permissions_pkey;
       public                 postgres    false    223                       2606    18625     printed_books printed_books_pkey 
   CONSTRAINT     c   ALTER TABLE ONLY public.printed_books
    ADD CONSTRAINT printed_books_pkey PRIMARY KEY (item_id);
 J   ALTER TABLE ONLY public.printed_books DROP CONSTRAINT printed_books_pkey;
       public                 postgres    false    233                       2606    18572 $   research_papers research_papers_pkey 
   CONSTRAINT     g   ALTER TABLE ONLY public.research_papers
    ADD CONSTRAINT research_papers_pkey PRIMARY KEY (item_id);
 N   ALTER TABLE ONLY public.research_papers DROP CONSTRAINT research_papers_pkey;
       public                 postgres    false    230                       2606    18378    reservations reservations_pkey 
   CONSTRAINT     h   ALTER TABLE ONLY public.reservations
    ADD CONSTRAINT reservations_pkey PRIMARY KEY (reservation_id);
 H   ALTER TABLE ONLY public.reservations DROP CONSTRAINT reservations_pkey;
       public                 postgres    false    228            �           2606    18312 &   role_permissions role_permissions_pkey 
   CONSTRAINT     x   ALTER TABLE ONLY public.role_permissions
    ADD CONSTRAINT role_permissions_pkey PRIMARY KEY (role_id, permission_id);
 P   ALTER TABLE ONLY public.role_permissions DROP CONSTRAINT role_permissions_pkey;
       public                 postgres    false    224    224            �           2606    18271    roles roles_pkey 
   CONSTRAINT     S   ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (role_id);
 :   ALTER TABLE ONLY public.roles DROP CONSTRAINT roles_pkey;
       public                 postgres    false    220            �           2606    18273    roles roles_role_name_key 
   CONSTRAINT     Y   ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_role_name_key UNIQUE (role_name);
 C   ALTER TABLE ONLY public.roles DROP CONSTRAINT roles_role_name_key;
       public                 postgres    false    220            �           2606    18279    user_roles user_roles_pkey 
   CONSTRAINT     f   ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT user_roles_pkey PRIMARY KEY (user_id, role_id);
 D   ALTER TABLE ONLY public.user_roles DROP CONSTRAINT user_roles_pkey;
       public                 postgres    false    221    221            �           2606    18259    users users_email_key 
   CONSTRAINT     Q   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);
 ?   ALTER TABLE ONLY public.users DROP CONSTRAINT users_email_key;
       public                 postgres    false    218            �           2606    18255    users users_pkey 
   CONSTRAINT     S   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);
 :   ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
       public                 postgres    false    218            �           2606    18257    users users_username_key 
   CONSTRAINT     W   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);
 B   ALTER TABLE ONLY public.users DROP CONSTRAINT users_username_key;
       public                 postgres    false    218                       1259    18725    idx_borrow_records_date    INDEX     Y   CREATE INDEX idx_borrow_records_date ON public.borrow_records USING btree (borrow_date);
 +   DROP INDEX public.idx_borrow_records_date;
       public                 postgres    false    241                       1259    18724    idx_borrow_records_user    INDEX     U   CREATE INDEX idx_borrow_records_user ON public.borrow_records USING btree (user_id);
 +   DROP INDEX public.idx_borrow_records_user;
       public                 postgres    false    241                       1259    18723    idx_items_author    INDEX     G   CREATE INDEX idx_items_author ON public.items USING btree (author_id);
 $   DROP INDEX public.idx_items_author;
       public                 postgres    false    235                       1259    18722    idx_items_genre    INDEX     B   CREATE INDEX idx_items_genre ON public.items USING btree (genre);
 #   DROP INDEX public.idx_items_genre;
       public                 postgres    false    235                       1259    18428    idx_reservations_user    INDEX     Q   CREATE INDEX idx_reservations_user ON public.reservations USING btree (user_id);
 )   DROP INDEX public.idx_reservations_user;
       public                 postgres    false    228            �           1259    18425    idx_users_email    INDEX     B   CREATE INDEX idx_users_email ON public.users USING btree (email);
 #   DROP INDEX public.idx_users_email;
       public                 postgres    false    218            '           2606    18698 *   borrow_records borrow_records_item_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.borrow_records
    ADD CONSTRAINT borrow_records_item_id_fkey FOREIGN KEY (item_id) REFERENCES public.items(item_id);
 T   ALTER TABLE ONLY public.borrow_records DROP CONSTRAINT borrow_records_item_id_fkey;
       public               postgres    false    235    4879    241            (           2606    18693 *   borrow_records borrow_records_user_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.borrow_records
    ADD CONSTRAINT borrow_records_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);
 T   ALTER TABLE ONLY public.borrow_records DROP CONSTRAINT borrow_records_user_id_fkey;
       public               postgres    false    218    4848    241            )           2606    18717 !   fines fines_borrow_record_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.fines
    ADD CONSTRAINT fines_borrow_record_id_fkey FOREIGN KEY (borrow_record_id) REFERENCES public.borrow_records(record_id);
 K   ALTER TABLE ONLY public.fines DROP CONSTRAINT fines_borrow_record_id_fkey;
       public               postgres    false    4887    241    243            *           2606    18712    fines fines_user_id_fkey    FK CONSTRAINT     |   ALTER TABLE ONLY public.fines
    ADD CONSTRAINT fines_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);
 B   ALTER TABLE ONLY public.fines DROP CONSTRAINT fines_user_id_fkey;
       public               postgres    false    243    4848    218            %           2606    18679 *   item_observers item_observers_item_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.item_observers
    ADD CONSTRAINT item_observers_item_id_fkey FOREIGN KEY (item_id) REFERENCES public.items(item_id);
 T   ALTER TABLE ONLY public.item_observers DROP CONSTRAINT item_observers_item_id_fkey;
       public               postgres    false    4879    239    235            &           2606    18674 *   item_observers item_observers_user_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.item_observers
    ADD CONSTRAINT item_observers_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);
 T   ALTER TABLE ONLY public.item_observers DROP CONSTRAINT item_observers_user_id_fkey;
       public               postgres    false    218    4848    239            "           2606    18636    items items_author_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.items
    ADD CONSTRAINT items_author_id_fkey FOREIGN KEY (author_id) REFERENCES public.authors(author_id);
 D   ALTER TABLE ONLY public.items DROP CONSTRAINT items_author_id_fkey;
       public               postgres    false    235    4864    226            #           2606    18658 (   notifications notifications_item_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_item_id_fkey FOREIGN KEY (item_id) REFERENCES public.items(item_id);
 R   ALTER TABLE ONLY public.notifications DROP CONSTRAINT notifications_item_id_fkey;
       public               postgres    false    4879    237    235            $           2606    18653 (   notifications notifications_user_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);
 R   ALTER TABLE ONLY public.notifications DROP CONSTRAINT notifications_user_id_fkey;
       public               postgres    false    4848    218    237            !           2606    18379 &   reservations reservations_user_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.reservations
    ADD CONSTRAINT reservations_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE CASCADE;
 P   ALTER TABLE ONLY public.reservations DROP CONSTRAINT reservations_user_id_fkey;
       public               postgres    false    218    4848    228                       2606    18318 4   role_permissions role_permissions_permission_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.role_permissions
    ADD CONSTRAINT role_permissions_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES public.permissions(permission_id) ON DELETE CASCADE;
 ^   ALTER TABLE ONLY public.role_permissions DROP CONSTRAINT role_permissions_permission_id_fkey;
       public               postgres    false    224    223    4860                        2606    18313 .   role_permissions role_permissions_role_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.role_permissions
    ADD CONSTRAINT role_permissions_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(role_id) ON DELETE CASCADE;
 X   ALTER TABLE ONLY public.role_permissions DROP CONSTRAINT role_permissions_role_id_fkey;
       public               postgres    false    224    220    4852                       2606    18290 &   user_roles user_roles_assigned_by_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT user_roles_assigned_by_fkey FOREIGN KEY (assigned_by) REFERENCES public.users(user_id);
 P   ALTER TABLE ONLY public.user_roles DROP CONSTRAINT user_roles_assigned_by_fkey;
       public               postgres    false    4848    218    221                       2606    18285 "   user_roles user_roles_role_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT user_roles_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(role_id) ON DELETE CASCADE;
 L   ALTER TABLE ONLY public.user_roles DROP CONSTRAINT user_roles_role_id_fkey;
       public               postgres    false    4852    221    220                       2606    18280 "   user_roles user_roles_user_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT user_roles_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE CASCADE;
 L   ALTER TABLE ONLY public.user_roles DROP CONSTRAINT user_roles_user_id_fkey;
       public               postgres    false    4848    221    218            �   �  x�=�A��0E��)x� (
�,:�b�ig3@�Ɇ�h��Dz$*�w�F�ד�R�.-}~�����|E��g�s��޿�=j`[�*���cę@'x]0� ��O�� E�]~s7��(^kB���B�A����l͵�q�O�Õ�( ��R,� 0��7�Y�r���gW����k���>��֚p]x\�k�@�+'vWW}�Z�ף�?�<�&���<�W�\��2C� c���"� fi�h�F�;	�G] ���UsMw�
�4ߣ�q����,���ދ�;������ȍ��_�|���w��&Nɧ1�
W�K��t|��v��5q���o6�� �F6��yg�+�(�z�{i�wna��+�F���_�*>0Dj�Ic�k_�b�@�tc����ُf�����e:����CK��      �   �  x�]TMo�6=˿b�C{�M[,ڣ���v�"�,
�2��4���a`�F�^I�8M�`Y�3o�{÷�vC�]�i�!�I����`y�+ˑ=~'��_��~�^�>���c{�DLiШyd����)�-K���8�4���pk%�1��~�F����z�Q�C�d=S���k��WO���#]����S[�{I�r��S��l�Z�7��g�����l����˫)���:DI''M<MH ���[�z�/��w��K%�$Nb�
�!�h0��zԖ�C�����x*��Q�ͨ�'�Zjk�,g<��ٜ��ֲ��S�_'rz2��n�оCJr����Gq��N��&��������^Y�q����T�ట�W?6�<X�u�������4;0M�OQ�pl����F�������t�)�{���ӷ�4�g��lFF�0��ֲV����It��N��CF,e�9�1��ڱ:���`��ZS�Q{)l�3�u���CU��s:\G�)/RW9@?$�n�ߟ�*� ��j�kЕ-Jߩ��]��g%�3	�k����_x[E)�xp xI�.|CG��3������õB�Z]E_�m�4.�ڱ�n�c�~nn��a�W��a�H�sqMR����%fi�5b^��;�#ƪ��WA�C9,��|�j0�9x�m��c穋�ei�����;�}�@���⧁c��ٹ���!r���(�m0�)����z��U��ң�ݘ�\2��8��He 2W��^��}��1��R��c�B������D��K���x��"���Q=n&�9�X�+�m� �3.�\#f�<�)�n����q�cR���BR�s/��\a!�j��\/U�)Ѓ�jk6y\��Y�V�@@-      �   �   x���K
�0�q�%������u���Ot�K;h�!\*$����=����:�W梀����������-i	�qGp�|+�cБ$Yڐ��"A&0o�NM<ȩ�S�����'���u]Կ�ͯg'�+�Ű�*�n����8��4���fV#�������I      �   ^  x�UQ���0�w�b�4w�Eܣ�� E�.�P2eі)C�w���א�g����ʭ^.2Qϖ�^�4k(m]$����c�ӌ��à�?FdY��N�,X��:���/�-��iL�����4cơh=\����掰��!�żuA+��X6��*`t~s����������Od�f_�A*_��'TN�1r��r�V��Y;��Z��r��h�f*I� H��ÎU�j�����±	�G�\y�r���$�G���Qk�|���E�>�L�D�,䥏��2<)DCZX=#��Mx5\�_�������(jS�$�����w���>�\�d��u)��H3*���r��/�������2      �   -   x�3�44�42�z��y��)�FF����@�?�=... �<�      �   :   x�34�4����/�L�LM�4202�50�54P04�22�21�3��476�4������  �
J      �   H  x�u�OO�@��ç��єh�����V4-��^����n
�dYL��1���&y���=�V����Y&ߨ<�g\��%�:��Ղ���I�ǝdVj�7�#e����ԇ��%}�Vm&�Z볳�Tp���	]�.���3ȥ��`O�Otl��<�9D��`�b���1�'�>Y�q��a������E?�0�#�>X΄],�h��.�F�����{W<��%����m��f���\2d��Z%]�o81��8&�����)�+��J��x�4[*��q/-�N�4ҶT��J��H�83�ZX@�5���G����_�����.      �     x�͒MK�@�ϻ�bn=T���޽ij�6%�x�vm1-��n��'��=���0H�C��i뗦mƉT���aQ�?f�
�2�vU��}Ylʻ�6�m�)�`�\ހK![�U^�0�_p������xH����w���G�Mw$�}��x@�R2����
��as�����Xa���80�	��{a���8�A:�8:㩞�8�AȀ����)j��r�"�e�2�ڋ8��%���Է�q���}��! 2Qp�P�R����x��Zn�3��� ��a�      �   v  x����n� ���)�_����kﶛ���rl��c ���DF[�-�;�;��;��sКA����{Yb���A
S�q�	w��@����(ݦ�>/azL� &������O�c3Y��9��ETB2T
{֜-s^���+Z*�o��:͝B�?=���)Q�Au0�t��\�y�b�$W��5�����@7,��.j����P���v�J��7R񚟀��Nu�,ƦV�ڬ�<x��#��zEQH�L�nCS�5�t��8-����jX�i�T�X,\��������qSv��Ba��d2v^ɚ�7C>�O�l4T��h�d'K8�ӝ��
TF?�n=�Q���2.%�˱.���Q�b�#�rk��^�~m� �Z�l�      �   7   x�3�4���4�4�0�t44�542�4�4�2I����ZA%�9M9M�b���� �	5      �   y   x����0ki���UVH�"p醠i��L"$�G�p�H{U�Pn���൏��<�/�jjQ��B#+��8��c)2<�4�
58�J���=M�B�m�&4�bb��t������29      �      x������ � �      �   �   x��ѻ�0��ښ"}`�I�1���#� w�����УI�S���R]f+�����X&��H����w��w Yy�32��/��F���M|��51�ib������:����!r<"r="r>"r?" )���%0��M�7"	��HD$"� I�hd�� ��J5�D��7��j�6b/b�b�b�b�b�b�b���J5��JU�TvMt�k)��.F�      �   '  x���=O�0�g�W���т�$�`be�8��Tǎ�KK�=N��1lg��<�kg�(�����*@�)����,y4Pzw	l@[���2����)�<���t�I�e�"?�CQ��C�?i�� CEV��Bw��8T���٥�Q5�����)zݒWo?B��W`�MD�m	z�ɇ�E��?�n�jԃ�Q���<�O����=k4f��Qu;��u�n�+åG�h�'Zl4
�|�fG=%XGp�
;���-O
�����P�DL�|ai�vV�3�����A���u��6I�_ǩ��      �   �   x��ѽ� ��O�>���4D&��s��n�?��Ը1��P_���(d4��`��7�s\J���F��M�7�5:9�bw�d�y��#<:XK;xX��Eӳ�B�.�S������.�!��eW�!��/�#�=�}C�T������1�0rY�!^ౌE6b {-%d(t,{H�t;l����b|      �   �  x���Y��J�k�}1w'���ո�;�KN2)ZYT��[g�m��81���"/oV���Ot]я�9���_F2�4�-P���7���������L��ve�{Gg���Y���dX�OZ�����6)2K�T�ʸ.�� ����D��Q��ʿ]EZ�p���2�����&��)�V�V�,L@7��u�{�`�"w�:rq�U����.���b������
�
�bh��W�����ݷ]Y=�-v�7�g���CzrN�iѱj���3����=��1u{���\� ܠ\c:���\���� ��5�9#�6�K���ۛ�	�+�2O;\4�W�8u���4茻abj����'����V�A�l�l@*K��u��B�+��<?��A���F	r�N[���:qr��ǰQ`�b�ux��QX�8�b�ۜ,kK#�����Bmx��U;���?�M����(e ߡ��C��{t�"T!T<?:ʼֻ6���s����,�I;�L��Kq���l��mɂ�9����
��ȥ�5y7��9��t"������J�)K�'���c������t�$�1䯩�n���Ww�A՝���L��@?�]t��g�ފJ����T����d�Q�0��䉴]ȗ�'#WT��%2Tv~�I�Ϥ�� ����g�S��mFj��*�w*M��O�qRk�
&'�������m�Y���-�0L� ��1T�B�4 0��I�qސKIt�c��٭w���
%rb'ߜ��I��m�z�Y^o=�}�v:�:I���5�w+�zۮ�am]�ffT-n����.	������J>f�edy��ԕ�����Cė��y�8�
���-��Svq*�j��K�C_;�A��:��q��bZ\o����)H!a�yw�<�O��K�B�$�Z���yLg��7�3�89ii��=��qC��:�3k'�� �v��L:g�`��b�`�g'�� &� ��<��^L2R�b��Mw���呾���(9�7}�Y��}m4}��`�侰
��j��]\Hua�f��_k���j:����;��|h�r�{�P��{/��U���7�-�x`�8�I�S��v�~i��E�y����
c;n�KoKޒ�( Q�.�;�����[���| R�|������~�     