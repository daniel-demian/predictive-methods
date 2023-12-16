import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn
import numpy as np
from matplotlib.animation import FuncAnimation

counter = 0

def init():
    sn.heatmap(corr_data, cbar=True, mask=matrix, annot=True, annot_kws={'size': 8}, ax=ax)
    ax.set_title('Correlation Heatmap', size=20, weight='bold')

def recalculate():
    global corr_data
    data = pd.read_csv("./data/new_data.csv", delimiter=';')
    data = data.drop(data.columns[-2], axis=1)
    corr_data = data.corr()

"""
def recalculate_if_specific_value_changed():
    global corr_data, previous_specific_value
    data = pd.read_csv("./data/new_data.csv", delimiter=';')
    data = data.drop(data.columns[-2], axis=1)
    
    # Extract the specific value you want to monitor
    current_specific_value = data.loc[0, 'specific_column_name']
    
    if current_specific_value != previous_specific_value:
        # The specific value has changed, recalculate corr_data
        corr_data = data.corr()
        previous_specific_value = current_specific_value
"""

def animate(i):
    global counter
    if counter % 5 == 0:
        recalculate()
    counter += 1
    ax.clear()
    sn.heatmap(corr_data, cbar=False, mask=matrix, annot=True, annot_kws={'size': 8}, ax=ax)
    ax.set_title('Correlation Heatmap', size=20, weight='bold')

data = pd.read_csv("./data/new_data.csv",delimiter=';')
data = data.drop(data.columns[-2], axis=1)
corr_data = data.corr()

sn.set(font_scale=0.8)
matrix = np.triu(corr_data)
fig, ax = plt.subplots(figsize=(7, 5))
ax.set_title('Correlation Heatmap', size=20, weight='bold')

anim = FuncAnimation(fig=fig, init_func=init, func=animate, interval=1000, cache_frame_data=False, repeat=False)

plt.show()


