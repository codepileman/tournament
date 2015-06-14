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
    conn =  connect()
    cur = conn.cursor()
    cur.execute("""delete from match""")
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn =  connect()
    cur = conn.cursor()
    cur.execute("""delete from player""")
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn =  connect()
    cur = conn.cursor()
    cur.execute("""select count(*) from player""")
    n = int(cur.fetchone()[0])
    conn.close()
    return n


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the players full name (need not be unique).
    """
    conn =  connect()
    cur = conn.cursor()
    cur.execute("""insert into player(name,matches,wins) values(%s,0,0)""",(name,))
    conn.commit()
    conn.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player unique id (assigned by the database)
        name: the player full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn =  connect()
    cur = conn.cursor()
    cur.execute("""select * from player order by wins DESC""")
    allPlayer = cur.fetchall()
    return allPlayer

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn =  connect()
    cur = conn.cursor()
    cur.execute("""update player set wins=wins+1, matches=matches+1 where pid = %s""",(winner,))
    cur.execute("""update player set matches=matches+1 where pid = %s """,(loser,))
    conn.commit()
    conn.close() 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player unique id
        name1: the first player name
        id2: the second player unique id
        name2: the second player name
    """
    conn =  connect()
    cur = conn.cursor()
    cur.execute("""select id, name from player order by wins/matches DESC""")
    allplay = cur.fetchall()
    ls = []
    i = 0
    while i < len(allplay):
        ls.append((allplay[i],allplay[i+1])
        i = i + 2

    return ls
        



