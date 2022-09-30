import pandas as pd
import psycopg2
import matplotlib.pyplot as plt


if __name__ == '__main__':
    df = pd.read_csv("../data+/2_neighbourhood.csv")
    #conn = psycopg2.connect(
    #    host="85.214.90.195",
    #    port=5532,
    #    database="postgres",
    #    user="postgres",
    #    password="digitus"
    #)

    #artists = pd.read_sql("SELECT id,popularity FROM artists", conn)
    #temp = pd.merge(right=df, left=artists, right_on='artist_id', left_on='id')

    plt.scatter(df["popularity"], df["1_n"])
    plt.scatter(df["popularity"], df["2_n"])
    plt.show()
    pass