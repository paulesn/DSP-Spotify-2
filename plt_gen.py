import matplotlib.pyplot as plt
import pickle

with open("data+/all_subgraphs.pickle", 'rb') as pickle_file:
    subnets = pickle.load(pickle_file)

graph_size = []
average_follower = []
average_popularity = []
genre_size = []
random_bool = True
for graph in subnets:
    if random_bool:
        random_bool = False
        continue
    graph_size.append(graph.no_of_nodes)
    average_popularity.append(graph.popularity['AVG(popularity)'][0])
    average_follower.append(graph.followers['AVG(followers)'][0])
    print(graph.genres)
    genre_size.append(graph.genres['genre_id'].__len__())

plt.scatter(graph_size, genre_size)
ax = plt.gca()
#ax.set_yscale('log')
#ax.set_xscale('log')
plt.show()
