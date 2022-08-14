import networkx
import pandas as pd
import sqlite3


class Subgraph:

    def identify_genres(self, nodes):
        con = sqlite3.connect("spotify.sqlite")
        con.text_factory = str
        genres = pd.read_sql_query(
            f"""SELECT genre_id, COUNT(genre_id)
            FROM r_artist_genre
            WHERE artist_id IN ({str(nodes)[1:-1]})
            GROUP BY genre_id;""",
            con)
        con.close()
        self.genres = genres.to_dict()

    def identify_popularity(self, nodes):
        con = sqlite3.connect("spotify.sqlite")
        con.text_factory = str
        pop = pd.read_sql_query(
            f"""SELECT AVG(popularity), MAX(popularity), MIN(popularity)
                    FROM artists
                    WHERE id IN ({str(nodes)[1:-1]});""",
            con)
        con.close()
        self.popularity = pop.to_dict()

    def identify_follower(self, nodes):
        con = sqlite3.connect("spotify.sqlite")
        con.text_factory = str
        follow = pd.read_sql_query(
            f"""SELECT AVG(followers), MAX(followers), MIN(followers)
                    FROM artists
                    WHERE id IN ({str(nodes)[1:-1]});""",
            con)
        con.close()
        self.followers = follow.to_dict()

    def generate_dict(self):
        return {
            'number of nodes': self.no_of_nodes,
            'number of edges': self.no_of_edges,
            'max popularity': self.popularity['MAX(popularity)'],
            'avg popularity': self.popularity['AVG(popularity)'],
            'min popularity': self.popularity['MIN(popularity)'],
            'max followers': self.followers['MAX(followers)'],
            'avg followers': self.followers['AVG(followers)'],
            'min followers': self.followers['MIN(followers)'],
            'genres': self.genres.__len__(),
        }

    def __init__(self, graph, nodes):
        self.graph = graph
        self.no_of_nodes = graph.__len__()
        self.no_of_edges = graph.size()
        self.identify_genres(nodes)
        self.identify_popularity(nodes)
        self.identify_follower(nodes)
