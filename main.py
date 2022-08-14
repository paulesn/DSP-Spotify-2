import networkx as nx
import pandas as pd
import sqlite3
import pickle
from datetime import datetime
from Subgraph import Subgraph

filtered = """
SELECT r1.artist_id AS source, r2.artist_id AS target
    FROM r_track_artist r1, r_track_artist r2, artists a1, artists a2
    WHERE r1.track_id = r2.track_id
    AND r1.artist_id < r2.artist_id
    AND r1.artist_id = a1.id AND a1.popularity > 0
    AND r2.artist_id = a2.id AND a2.popularity > 0
"""
unfiltered = """
SELECT r1.artist_id AS source, r2.artist_id AS target 
    FROM r_track_artist r1, r_track_artist r2 
    WHERE r1.track_id = r2.track_id 
    AND r1.artist_id < r2.artist_id
"""

now = datetime.now()

current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)

con = sqlite3.connect("spotify.sqlite")
con.text_factory = str
df = pd.read_sql_query(
    filtered,
    con)
con.close()

print(df)
df.to_csv("dataframe")
now = datetime.now()

current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)

graph = nx.from_pandas_edgelist(df, 'source', 'target')
nx.write_edgelist(graph, "data+/graph_edgelist")

now = datetime.now()

current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)
now = datetime.now()

###################
i = 0
subgraphs = {}
all = []
all_subg = []
for g in nx.connected_components(graph):
    sgl = graph.subgraph(g).__len__()
    i += 1
    if sgl in subgraphs:
        subgraphs[sgl] += 1
    else:
        subgraphs[sgl] = 1
    this_sub = Subgraph(graph.subgraph(g), g)
    all_subg.append(this_sub)
    all.append(this_sub.generate_dict())
all = pd.DataFrame(all)
print(i)
sdf = pd.Series(subgraphs)
print(sdf)
with open('data+/all_subgraphs.pickle', 'wb') as f:
    pickle.dump(all_subg, f)
pass
