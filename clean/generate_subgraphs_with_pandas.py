import psycopg2
import pandas as pd
from datetime import datetime


if __name__ == '__main__':
    conn = psycopg2.connect(
            host="85.214.90.195",
            port=5532,
            database="postgres",
            user="postgres",
            password="digitus"
        )

    rta = pd.read_sql("SELECT * from r_track_artist", conn)
    tracks = pd.read_sql("SELECT * from tracks WHERE popularity > 0", conn)
    artists = pd.read_sql("SELECT * FROM artists WHERE popularity > 0", conn)

    temp = pd.merge(left=rta,right=artists,left_on="artist_id", right_on="id")
    temp = pd.merge(left=temp,right=tracks,left_on="track_id", right_on="id")

    edge_list = temp[["track_id", "artist_id"]]
    edge_list = pd.merge(left=edge_list,right=edge_list,left_on="track_id",right_on="track_id")
    edge_list = edge_list.drop(["track_id"],axis=1)
    edge_list = edge_list[edge_list["artist_id_x"] != edge_list["artist_id_y"]]

    data = pd.merge(left=edge_list, right=artists[["id", "popularity"]], right_on="artist_id_y")

    groups = data.groupby("artist_id_x")

    map = {}
    count = 0

    for element in groups:
        print(f"group no. {count} [{datetime.now()}]")
        count += 1

    pass