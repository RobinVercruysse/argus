CREATE DATABASE IF NOT EXISTS wirelesswatch;

CREATE TABLE IF NOT EXISTS wirelesswatch.Station (
    mac VARCHAR(17) primary key
);

CREATE TABLE IF NOT EXISTS wirelesswatch.StationName (
    mac VARCHAR(17) not null,
    name VARCHAR(255) not null,
    primary key (mac, name),
    foreign key (mac) references wirelesswatch.Station (mac)
);

CREATE TABLE IF NOT EXISTS wirelesswatch.Spot (
    transmitter_mac VARCHAR(17),
    receiver_mac VARCHAR(17),
    sig smallint not null default 0,
    spot_time timestamp not null,
    frame_type tinyint not null default -1,
    frame_subtype tinyint not null default -1,
    channel tinyint not null default 0,
    foreign key (transmitter_mac) references wirelesswatch.Station (mac),
    foreign key (receiver_mac) references wirelesswatch.Station (mac)
);