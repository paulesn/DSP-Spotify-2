import psycopg2
import pandas as pd
import pickle

query = """
SELECT *
FROM (r_track_artist a LEFT JOIN r_track_artist b ON a.track_id LIKE b.track_id) JOIN tracks ON a.track_id LIKE tracks.id
WHERE a.artist_id < b.artist_id;
"""


if __name__ == '__main__':

    conn = psycopg2.connect(
        host="85.214.90.195",
        port=5532,
        database="postgres",
        user="postgres",
        password="digitus"
    )
    #alq = create_engine(
    #    url="postgresql+psycopg2://postgres:digitus@85.214.90.195:5532/postgres'",
    #)
    df = pd.read_sql(query, conn)
    # store data to disk
    with open('../data+/tracks-pop.pickle', 'wb') as f:
        pickle.dump(df, f)


