import pandas as pd
import networkx as nx
import psycopg2
from datetime import datetime
import random

'''
This code is generating subgraphs for the filteres artists and nodes 
and tries to identify the 1 and 2 neighbourhood.
1 neigbourhood needs a half day
2 neigbourhood probably around 100 years
'''

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
    graph = nx.from_pandas_edgelist(df=edge_list,source="artist_id_x",target="artist_id_y")

    list_of_subgraphs = []
    for c in nx.connected_components(graph):
         list_of_subgraphs.append(graph.subgraph(c))

    sg = list_of_subgraphs[1]
    map = {}
    map2 = {}
    grap_count = 0

    random.seed("Data Science with Python")

    for subgraph in list_of_subgraphs:
        print(f"graph number {grap_count} ({subgraph.__len__()} nodes) [{datetime.now()}]")
        node_um = 0
        grap_count += 1
        for base_node in subgraph:
            print(f"Node {node_um} {datetime.now()}")
            node_um += 1
            if random.randint(0, 100) != 2:
                continue
            sum = 0
            count = 0
            sum2 = 0
            count2 = 0
            for node in nx.all_neighbors(subgraph,base_node):
                # clalculate first neighourhood
                sum += artists[artists["id"] == node].popularity.reset_index(drop=True)[0]
                count +=1
                # calculate second neighbourhood
                temp_map = {}
                for node2 in nx.all_neighbors(subgraph,node):
                    if node == base_node:
                        # no need to include the base node in the neighbourhood
                        continue
                    temp_map[node2] = artists[artists["id"] == node2].popularity.reset_index(drop=True)[0]

                for i in temp_map.values():
                    sum2 += i
                    count2 += 1

            map[base_node] = (sum/count)
            map2[base_node] = (sum2/count2)
    df2 = pd.merge(right=pd.DataFrame([map, map2]).transpose().reset_index(),
                   left=artists[["id", "popularity"]],
                   left_on="id",
                   right_on="index"
                   )

    pass




