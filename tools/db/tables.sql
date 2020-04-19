-- cd C:\PostgreSQL\pg11\bin
-- psql -h localhost -d postgres -U postgres -w
--
-- ALTER USER postgres WITH PASSWORD 'python';
-- CREATE USER test WITH PASSWORD 'python';
-- \du - посмотреть список пользователей (ролей)
-- ALTER USER test WITH SUPERUSER;
-- CREATE DATABASE test;
-- create schema test


create sequence test.seq_spr_scl_f_id;
create table test.spr_scl
(
	-- Only integer types can be auto increment
	f_id numeric default nextval('test.seq_spr_scl_f_id') not null
		constraint spr_scl_pk
			primary key,
	f_cod numeric not null,
	f_name varchar(50) default ' ' not null
);

create unique index spr_scl_f_cod_uindex
	on test.spr_scl (f_cod);

create sequence if not exists test.seq_docs_f_id;
create table test.docs
(
    -- Only integer types can be auto increment
    f_id       numeric              default nextval('test.seq_docs_f_id') not null
        constraint docs_pk
            primary key,
    f_num_doc  varchar(10) not null,
    f_date_doc date,
    f_sclad    numeric,
    f_is_ready numeric(1)  not null default 0,
    constraint docs_sclad FOREIGN KEY (f_sclad)
        REFERENCES test.spr_scl (f_cod)
);

insert into spr_scl (f_cod, f_name) values (1, 'Склад1');
insert into spr_scl (f_cod, f_name) values (1, 'Склад2');
insert into spr_scl (f_cod, f_name) values (1, 'Склад3');
insert into spr_scl (f_cod, f_name) values (1, 'Склад4');
insert into spr_scl (f_cod, f_name) values (1, 'Склад5');

insert into docs (f_num_doc, f_date_doc, f_sclad, f_is_ready) values ('Б1', to_date('15/03/2020', 'dd_mm_yyyy'), 1, 0);
insert into docs (f_num_doc, f_date_doc, f_sclad, f_is_ready) values ('Б2', to_date('15/03/2020', 'dd_mm_yyyy'), 2, 1);


