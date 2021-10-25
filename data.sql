create table widgets (
    id serial not null primary key,
    name varchar(100)
);

insert into widgets (name)
VALUES 
    ('Apple'),
    ('Orange'),
    ('Grape');
