import psycopg2
import pandas as pd
import pickle


if __name__ == '__main__':

    conn = psycopg2.connect(
        host="85.214.90.195",
        port=5532,
        database="postgres",
        user="postgres",
        password="digitus"
    )
    # initial data loading
    rta = pd.read_sql("SELECT * FROM r_track_artist", conn)
    artist = pd.read_sql("SELECT * FROM artists WHERE popularity > 0", conn).drop("name", axis=1)

    aXa = pd.merge(rta, rta, on="track_id")\
        .drop("track_id", axis=1)
    groups = aXa.groupby("artist_id_x")
    groups_counted = groups.count()\
        .reset_index()\
        .rename(columns={"artist_id_y": "no_of_artists"})
    aXa = pd.merge(left=groups_counted, right=artist, left_on="artist_id_x", right_on="id")
    groups = aXa.drop(["artist_id_x", "id"], axis=1)\
        .rename(columns={"no_of_artists": "no_of_tracks"})\
        .groupby("no_of_tracks")
    groups_max = groups.max()
    groups_max = groups.max().reset_index()


    # store data to disk
    with open('../data+/artists-pop-foll.pickle', 'wb') as f:
        print("here")
        pickle.dump(groups, f)


