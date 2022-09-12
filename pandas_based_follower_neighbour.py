import sqlite3
import threading
from datetime import datetime
import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt


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

    artists = pd.read_sql_query("SELECT id, followers FROM artists", con)
    con.close()
    print(f"base data init finished {datetime.now()}")

    edge_list = r_track_artist.merge(r_track_artist, left_on="track_id", right_on="track_id")
    edge_list = edge_list[edge_list.artist_id_x > edge_list.artist_id_y].reset_index(drop=True)
    print(f"edge list created {datetime.now()}")

    foll_list = edge_list.merge(right=artists,left_on="artist_id_y", right_on="id")
    foll_list = foll_list[["artist_id_x","followers"]].rename(columns={"followers":"1-hop"})
    print(f"edge list reformated to foll list {datetime.now()}")

    groups = foll_list.groupby(["artist_id_x"]).mean()
    print(f"edge list grouped and mean calculated for 1-hop {datetime.now()}")
    df1 = groups.merge(right=artists, left_on="artist_id_x", right_on="id")[["followers","1-hop"]]

    ##############################################################
    # 2 - HOP
    ##############################################################

    foll_list = edge_list.merge(right=groups.reset_index(),left_on="artist_id_y", right_on="artist_id_x")
    foll_list = foll_list[["artist_id_x_x", "1-hop"]].rename(columns={"1-hop": "2-hop"})
    groups = foll_list.groupby(["artist_id_x_x"]).mean()
    print(f"created 2-hop {datetime.now()}")
    df2= groups.merge(right=artists, left_on="artist_id_x_x", right_on="id")[["followers","2-hop"]]

    ##############################################################
    # 3 - HOP
    ##############################################################

    foll_list2 = edge_list.merge(right=groups.reset_index(), left_on="artist_id_y", right_on="artist_id_x_x")
    foll_list2 = foll_list2[["artist_id_x_x", "2-hop"]].rename(columns={"2-hop": "3-hop"})
    groups = foll_list2.groupby(["artist_id_x_x"]).mean()
    print(f"created 3-hop {datetime.now()}")
    df3 = groups.merge(right=artists, left_on="artist_id_x_x", right_on="id")[["followers","3-hop"]]



    # store data to disk
    with open('data+/neigbour_for_scatter.pickle', 'wb') as f:
        pickle.dump((df1, df2, df3), f)

    # create scatter plot
    plt.scatter(df1['followers'], df1['1-hop'], c='red', alpha=0.3)
    plt.scatter(df2['followers'], df2['2-hop'], c='green', alpha=0.3)
    plt.scatter(df3['followers'], df3['3-hop'], c='blue', alpha=0.3)

    # calc linear regression

    b1, a1 = np.polyfit(df1['followers'], df1['1-hop'], deg=1)
    b2, a2 = np.polyfit(df2['followers'], df2['2-hop'], deg=1)
    b3, a3 = np.polyfit(df3['followers'], df3['3-hop'], deg=1)

    # Create sequence of 100 numbers from 0 to 100
    xseq = np.linspace(0, 10, num=100000)

    # Plot regression line
    plt.plot(xseq, b1 + a1 * xseq, color="red", lw=2.5);
    plt.plot(xseq, b2 + a2 * xseq, color="green", lw=2.5);
    plt.plot(xseq, b3 + a3 * xseq, color="blue", lw=2.5);

    ax = plt.gca()
    plt.xlabel('Follower of Node')
    plt.ylabel('Average Follower of neighborhood')
    ax.set_yscale('log')
    ax.set_xscale('log')
    plt.show()
