import sqlite3
import threading
from datetime import datetime
import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt

statement1 = """SELECT A.artist_id, AA.followers, AVG(BB.followers)
FROM r_track_artist as A, r_track_artist as B, artists as AA, artists as BB
WHERE A.track_id == B.track_id
AND A.artist_id == AA.id
AND B.artist_id == BB.id
AND AA.id != BB.id
GROUP BY A.artist_id"""

statement2 = """SELECT artists.followers, AVG(temp.out)
FROM r_track_artist as B, r_track_artist AS C, artists, (SELECT A.artist_id AS id, AA.followers, AVG(BB.followers) AS out
                                                            FROM r_track_artist as A, r_track_artist as B, artists as AA, artists as BB
                                                            WHERE A.track_id == B.track_id
                                                            AND A.artist_id == AA.id
                                                            AND B.artist_id == BB.id
                                                            GROUP BY A.artist_id) AS temp
WHERE B.track_id == C.track_id
AND B.artist_id == artists.id
AND C.artist_id == temp.id
GROUP BY B.artist_id"""

statement3 = """
SELECT artists.followers, AVG(temp2.out2) as fout
FROM artists, r_track_artist as AAA, r_track_artist as BBB,
    (SELECT id2, artists.followers, AVG(temp.out) as out2
FROM r_track_artist as B, r_track_artist AS C, artists, (SELECT A.artist_id AS id2, AA.followers, AVG(BB.followers) AS out
                                                            FROM r_track_artist as A, r_track_artist as B, artists as AA, artists as BB
                                                            WHERE A.track_id == B.track_id
                                                            AND A.artist_id == AA.id
                                                            AND B.artist_id == BB.id
                                                            GROUP BY A.artist_id) AS temp
WHERE B.track_id == C.track_id
AND B.artist_id == artists.id
AND C.artist_id == temp.id2
GROUP BY B.artist_id) as temp2

WHERE AAA.artist_id == artists.id
AND BBB.artist_id == temp2.id2
AND AAA.artist_id == BBB.artist_id
GROUP BY AAA.artist_id
"""

'''
This file loads all nodes, their amount of followers and 
the average of followers of the sourrounding nodes
'''

if __name__ == '__main__':

    print(f"init base data {datetime.now()}")

    # load SQL query
    con = sqlite3.connect("data+/spotify.sqlite")
    con.text_factory = str
    r_track_artist = pd.read_sql_query("SELECT * FROM r_track_artist", con)
    artists = pd.read_sql_query("SELECT * FROM artists", con)
    con.close()
    print(f"base data init finished {datetime.now()}")

    edge_list = r_track_artist.merge(r_track_artist, left_on="track_id", right_on="track_id")
    print(f"edge list created {datetime.now()}")

    edge_list = edge_list.groupby(1)
    print(f"edge list grouped {datetime.now()}")

    # store data to disk
    with open('data+/neigbour_for_scatter.pickle', 'wb') as f:
        pickle.dump((df1, df2, df3), f)

    # create scatter plot
    plt.scatter(df1['followers'], df1['AVG(BB.followers)'], c='red', alpha=0.3)
    plt.scatter(df2['followers'], df2['AVG(temp.out)'], c='green', alpha=0.3)
    plt.scatter(df3['followers'], df3['fout'], c='blue', alpha=0.3)

    # calc linear regression

    b1, a1 = np.polyfit(df1['followers'], df1['AVG(BB.followers)'], deg=1)
    b2, a2 = np.polyfit(df2['followers'], df2['AVG(temp.out)'], deg=1)
    b3, a3 = np.polyfit(df3['followers'], df3['fout'], deg=1)

    # Create sequence of 100 numbers from 0 to 100
    xseq = np.linspace(0, 10, num=10000)

    # Plot regression line
    plt.plot(xseq, a1 + b1 * xseq, color="red", lw=2.5);
    plt.plot(xseq, a2 + b2 * xseq, color="green", lw=2.5);
    plt.plot(xseq, a3 + b3 * xseq, color="blue", lw=2.5);

    ax = plt.gca()
    plt.xlabel('Follower of Node')
    plt.ylabel('Average Follower of neighborhood')
    ax.set_yscale('log')
    ax.set_xscale('log')
    plt.show()
