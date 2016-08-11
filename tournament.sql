-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;
CREATE tournament;
\c tournament

CREATE TABLE player (
  player_id serial Primary Key,
  name varchar
 );

CREATE TABLE match (
  match_id serial Primary Key,
  winner integer references player(player_id) NOT NULL,
  loser integer references player(player_id) NOT NULL
);
--join in previous iterations gave false count
--code found at: https://github.com/p00gz/udacity-fullstack-swiss-tournament-P2/blob/master/vagrant/tournament/tournament.sql
CREATE OR REPLACE VIEW standings AS
SELECT player_id, name,
(SELECT COUNT (match.match_id) FROM match WHERE player.player_id = match.winner) as wins,
(SELECT COUNT (match.match_id) FROM match WHERE (player.player_id = match.winner OR player.player_id = match.loser)) as no_matches
FROM player
ORDER BY wins DESC, no_matches DESC
