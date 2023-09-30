"""
@Author: Rikesh Chhetri
@Date: 2021-09-12 
@Last Modified by: Rikesh Chhetri
@Last Modified time: 2021-09-12 10:03:30
@Title : Program Aim perform the plotting of Stock Data Prediction using Matplotlib Flask
"""


import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import style



style.use("seaborn")


output = pd.read_csv('p_data.csv')
count = len(output["time"])
index_count = 0

def getData():
    global count
    index_count
    if index_count <= count:
        print(index_count)
        return output.loc[index_count, "time"], output.loc[index_count, "close"], output.loc[index_count, "prediction"]



# Create figure for plotting
fig, ax = plt.subplots()


xs = []
y1 = []
y2 = []

def animate(i,xs:list, y1:list,y2:list):

    global index_count
    date, Close, prediction = getData()
    data = [date, Close, prediction]

    index_count+=1
    xs.append(data[0])
    y1.append(data[1])
    y2.append(data[2])

    xs = xs[-5:]
    y1 = y1[-5:]
    y2 = y2[-5:]
    ax.clear()
    ax.plot(xs,y1,'-bo',label="Close")
    ax.plot(xs,y2,'-go',label='Prediction')

    
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    ax.set_title("Stock Data Prediction")
    ax.set_xlabel("Time")
    ax.set_ylabel("Stock Price")
    ax.legend(loc='upper center')
    plt.tight_layout()
     
    

ani = FuncAnimation(fig, animate, fargs=(xs,y1,y2),interval=2000)
plt.show()






