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
df1 = []
df2 = []
df3 = []
df4 = []
if __name__ == '__main__':
    # load data from disk
    with open('data+/neigbour_for_scatter_median.pickle', 'rb') as f:
        (df1, df2, df3, df4) = pickle.load(f)

    # create scatter plot
    #plt.scatter(df1['followers'], df1['1-hop'], c='red', alpha=0.005)
    #plt.scatter(df2['followers'], df2['2-hop'], c='green', alpha=0.005)
    #plt.scatter(df3['followers'], df3['3-hop'], c='blue', alpha=0.005)

    # calc linear regression

    b1, a1 = np.polyfit(df1['followers'], df1['1-hop'], deg=1)
    b2, a2 = np.polyfit(df2['followers'], df2['2-hop'], deg=1)
    b3, a3 = np.polyfit(df3['followers'], df3['3-hop'], deg=1)
    b4, a4 = np.polyfit(df4['followers'], df4['4-hop'], deg=1)

    # Create sequence of 100 numbers from 0 to 100
    xseq = np.linspace(1, 1000, num=100000)

    # Plot regression line
    plt.plot(xseq, b1 + a1 * xseq, color="red", lw=2.5);
    plt.plot(xseq, b2 + a2 * xseq, color="green", lw=2.5);
    plt.plot(xseq, b3 + a3 * xseq, color="blue", lw=2.5);
    plt.plot(xseq, b4 + a4 * xseq, color="black", lw=2.5);

    ax = plt.gca()
    plt.xlabel('Follower of Node')
    plt.ylabel('Average Follower of neighborhood')
    #ax.set_yscale('log')
    #ax.set_xscale('log')
    plt.show()
