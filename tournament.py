#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    Db = connect()
    cursor = Db.cursor()
    query = ("DELETE FROM match;")
    cursor.execute(query)
    Db.commit()
    Db.close()



def deletePlayers():
    """Remove all the player records from the database."""
    Db = connect()
    cursor = Db.cursor()
    query = ("DELETE FROM player;")
    cursor.execute(query)
    Db.commit()
    Db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    Db = connect()
    cursor = Db.cursor()
    query = ("SELECT COUNT(player_id) from player")
    cursor.execute(query)
    no_of_players = cursor.fetchone()[0]
    Db.close()
    return no_of_players


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      first_name: the player's  name (need not be unique).
      last_name: the player's last name (need not be unique).
    """
    Db = connect()
    cursor = Db.cursor()
    query = ("INSERT INTO player(player_id, name) VALUES (default, %s);")
    cursor.execute(query,(name,))
    Db.commit()
    Db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    Db = connect()
    cursor = Db.cursor()
    query = ("SELECT * FROM standings")
    cursor.execute(query)
    current = cursor.fetchall()
    Db.close()
    return current




def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    Db = connect()
    cursor = Db.cursor()
    query = ("INSERT INTO match(match_id, winner, loser) VALUES (default, %s, %s);")
    cursor.execute(query, (winner,loser,))
    Db.commit()
    Db.close()



def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    Db = connect()
    cursor = Db.cursor()
    cursor.execute("SELECT player_id, name FROM standings ORDER BY wins desc;")
    result = cursor.fetchall()
    pair = []
    for i in range(0, len(result),2):
        players_list = result[i][0], result[i][0], result[i+1][0], result[i+1][1]
        pair.append(players_list)
    Db.close()
    return pair
