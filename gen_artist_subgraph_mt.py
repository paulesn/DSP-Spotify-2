import sqlite3
import threading
from datetime import datetime
import networkx as nx
import pandas as pd
import pickle
import matplotlib.pyplot as plt

class SearchSpace(threading.Thread):
    def __init__(self, space, name, dic, graph):
        threading.Thread.__init__(self)
        self.space = space
        self.name = name
        self.map = {}
        self.dic = dic
        self.graph = graph

    def run(self):
        print(f"Thread {self.name} started")
        for o in space:
            self.iter_nodes(o)

    '''
    This method expands a single node
    '''

    def iter_nodes(self, node):
        # timestamp
        time = datetime.now()
        # variables for this loop execution
        sum = 0
        num = 0
        # load followers of this node
        node_f = self.dic[node]
        # load all neigbours of node
        adjazent = nx.neighbors(nx.Graph(self.graph.graph), node)

        # calculate average of followers of all neigbours
        for a in adjazent:
            sum += self.dic[a]
            num += 1

        # prints the node follower and the average follower of direct collaborators
        print(f"[{self.name}]{node} ({node_f}): {sum / num}")

        self.map[node_f] = sum / num
        print(f"[{self.name}]{datetime.now() - time}")


if __name__ == '__main__':
    # load networkx graph from disk
    with open("data+/all_subgraphs.pickle", 'rb') as pickle_file:
        subnets = pickle.load(pickle_file)

    # list subgraphs bigger than x to identify subnets for tests
    i2 = 0
    for s in subnets:
        if s.no_of_nodes > 40:
            print(f"{i2}:{s.no_of_nodes}")
        i2 += 1

    # define variables for later
    node_followers = []
    adjacent_followers = []
    dic = {}

    # load SQL query
    con = sqlite3.connect("spotify.sqlite")
    con.text_factory = str
    df = pd.read_sql_query(
        f"SELECT id, followers FROM artists",
        con)
    con.close()
    # convert SQL query to dict
    dic = df.set_index('id').to_dict()['followers']

    # load first subnet. it is the biggest one
    s = subnets[0]
    print(f"density={nx.density(nx.Graph(s.graph))}")

    number_of_threads = 8
    list_of_all_nodes = list(s.graph)
    length_of_loan = len(list_of_all_nodes)
    area = (length_of_loan / number_of_threads)
    list_of_threads = []

    # generate a multiprocess pool and execute the iter_nodes function
    for i in range(8):
        a = int(i * area)
        b = int((i + 1) * area)
        space = list_of_all_nodes[a:b]
        thread = SearchSpace(space, i, dic, s)
        thread.start()
        list_of_threads.append(thread)

    for t in list_of_threads:
        t.join()

    # create scatter plot
    plt.scatter(node_followers, adjacent_followers)
    ax = plt.gca()
    plt.show()

    # store data to disk
    with open('data+/followers.pickle', 'wb') as f:
        pickle.dump((node_followers, adjacent_followers), f)
