import networkx as nx
import pickle
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

'''
this file is now for random small checks
'''

statement1 = """
SELECT id, name, followers, popularity, features
FROM artists join (SELECT A.artist_id, COUNT(A.track_id) as features
             FROM r_track_artist as A, r_track_artist as B
             WHERE A.track_id == B.track_id
             AND A.artist_id < B.artist_id
             GROUP BY A.artist_id) on artist_id == artists.id
"""

if __name__ == '__main__':
    con = sqlite3.connect("data+/spotify.sqlite")
    con.text_factory = str
    df = pd.read_sql_query(statement1, con)

    # create scatter plot
    plt.scatter(df['features'], df['popularity'], c='red', alpha=0.5)
    #plt.scatter(df['features'], df['followers'], c='green', alpha=0.005)
    # calc linear regression

    b1, a1 = np.polyfit(df['features'], df['popularity'], deg=1)
    b2, a2 = np.polyfit(df['features'], df['followers'], deg=1)

    # Create sequence of 100 numbers from 0 to 100
    xseq = np.linspace(1, 1000, num=100000)

    # Plot regression line
    plt.plot(xseq, b1 + a1 * xseq, color="black", lw=2.5);
    #plt.plot(xseq, b2 + a2 * xseq, color="green", lw=2.5);

    ax = plt.gca()
    plt.xlabel('Follower of Node')
    plt.ylabel('Average Follower of neighborhood')
    ax.set_yscale('log')
    ax.set_xscale('log')
    plt.show()