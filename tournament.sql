-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

--create player user
create table player (
	pid serial primary key,
	name VARCHAR(40) not null,
	wins int,
	matches int
	
);

create table match(
	mid serial primary key,
	winner_id int references player(pid),
	loser_id int references player(pid)
);

