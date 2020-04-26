create table state (
 chat_id int,
 location varchar(255),
 store_1 int,
 store_2 int,
 store_1_status tinyint,
 store_2_status tinyint,
 store_1_name varchar(255),
 store_2_name varchar(255),
 location_confirm tinyint,
 is_bot tinyint,
 first_name varchar(255),
 last_name varchar(255),
 PRIMARY KEY (chat_id)
);

create table store (
 id bigint auto_increment,
 chat_id int,
 store_id int,
 store_hash varchar(255),
 store_name varchar(255),
 location varchar(50),
 primary key (id),
 index store_index (store_id, store_hash),
 foreign key (chat_id) references state (chat_id)
);

create table store_status (
 date varchar(255),
 title varchar(255),
 store_hash varchar(255),
 is_open tinyint,
 price int,
 store_id int,
 store_name varchar(255),
 PRIMARY KEY (date, title, store_hash)
);
