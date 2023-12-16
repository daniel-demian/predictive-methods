import math

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.gridspec import GridSpec

#metoda pre precitanie dát z csv suboru
def read_data():
    data = pd.read_csv("./data/new_data.csv", delimiter=';')
    data = data.drop(data.columns[-2], axis=1)
    corr_data = data.corr()
    return data, corr_data

#metoda pre prepocitanie dat
def recalculate():
    data, corr_data = read_data()
    return data, corr_data

#metoda pre update heatmapy
def update_heatmap(ax, data, matrix, title):
    sns.heatmap(data, ax=ax, cbar=False, annot=True,
                annot_kws={'size': 8}, fmt=".2f", mask=matrix, cmap='coolwarm', vmin=-1, vmax=1)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=25)
    ax.set_title(title, size=15, weight='bold')

#metoda pre update regplotu
def update_regplot(ax, data, x, y, title, color, corrcoef):
    if corrcoef > 0.945:
        order = 1
    else:
        order = 2
    sns.regplot(x=x, y=y, data=data, ax=ax, order=order, color=color,
                line_kws={'color': 'red', 'linewidth': 1}, scatter_kws={'s': 10}, fit_reg=True)
    ax.set_title(title)

#funkcia vrati rozdiel a x, y (pressure, time) aby sa vedel vykreslit graf
def find_highest_difference(old_values, new_values):
    newValDict = {}
    j = 0
    for i in range(0, len(old_values)):
        if old_values.index[i][0] == new_values.index[i][0] and old_values.index[i][1] == new_values.index[i][1]:
            diff = abs(abs(old_values[i]) - abs(new_values[i]))
            newValDict[i] = diff
        else:
            diff = abs(0 - abs(new_values[i]))
            newValDict[i] = diff
        j = i

    for i in range(j+1, len(new_values)):
        diff = abs(0 - abs(new_values[i]))
        newValDict[i] = diff

    sorted_dict = sorted(newValDict.items(), key=lambda x: x[1], reverse=True)

    index = sorted_dict[0][0]
    valueChange = sorted_dict[0][1]
    old_value = 0
    for i in range(0, len(old_values)):
        if old_values.index[i][0] == new_values.index[index][0] and old_values.index[i][1] == new_values.index[index][1]:
            old_value = old_values[i]
    return valueChange, index, old_value

# funkcia vrati true, alebo false ak najde zmenu vačšiu ako 0.1
def check_if_changed(old, new, old_index):
    old_values = old.where(np.triu(np.ones(old.shape), k=1).astype(bool)).unstack().dropna()
    new_values = new.where(np.triu(np.ones(new.shape), k=1).astype(bool)).unstack().dropna()

    valueChange, index, old_value = find_highest_difference(old_values, new_values)

    if valueChange > 0.1:
        return valueChange, index, old_value

    return False, old_index, old_value

def percentage_rate(percent, data_len):
    return math.floor((percent * data_len) / 100.0)

if __name__ == "__main__":
    data, corr_data = read_data()
    changed = False
    old_corr_data = corr_data

    plt.ion()
    # Create a 2x4 grid of subplots
    fig = plt.figure(figsize=(13, 6))
    gs = GridSpec(2, 4, figure=fig)
    matrix = np.triu(corr_data)

    ax1 = fig.add_subplot(gs[0:2, 0:2])  # Spanning 2 rows and 2 columns

    ax2_1 = fig.add_subplot(gs[0, 2])  # 1st row, 1st column
    ax2_2 = fig.add_subplot(gs[0, 3])  # 1st row, 2nd column
    ax2_3 = fig.add_subplot(gs[1, 2])  # 2nd row, 1st column
    ax2_4 = fig.add_subplot(gs[1, 3])  # 2nd row, 2nd column

    plt.subplots_adjust(wspace=0.6, hspace=0.6)

    text = fig.text(0.5, 0.0001, '', ha='center', fontsize=10)

    # heatmap init
    sns.heatmap(corr_data, ax=ax1, cbar=True, annot=True,
                annot_kws={'size': 8}, fmt=".2f", mask=matrix, cmap='coolwarm', vmin=-1, vmax=1)

    ax1.clear()
    old_index = 0
    while True:
        new_data, new_corr_data = recalculate()
        changed, change_index, old_value = check_if_changed(corr_data, new_corr_data, old_index)

        if changed:
            data = new_data
            corr_data = new_corr_data

        # odstranenie duplikatov a diagonaly, nastavenie na NaN
        # zoradenie od najvacsieho po najmensie .abs() zaruci aj antikorelaciu
        # top_corr_values je v tvare (y,x,hodnota) vyberam prve styri
        corr_values = corr_data.where(np.triu(np.ones(corr_data.shape), k=1).astype(bool)).unstack().dropna()
        sorted_corr_values = corr_values.abs().sort_values(ascending=False)
        top_corr_values = sorted_corr_values.iloc[0:4]


        update_heatmap(ax1, corr_data, matrix, 'Correlation Heatmap')

        # top_corr_values.index[0][0] hodnota y
        # top_corr_values.index[0][1] hodnota x
        # top_corr_values.iloc[0] hodnota korelacie
        # print(top_corr_values.index[0][0], top_corr_values.index[0][1], top_corr_values.iloc[0])
        reg_ax = [ax2_1, ax2_2, ax2_3]
        for i in range(0, 3):
            update_regplot(reg_ax[i], data, x=top_corr_values.index[i][1], y=top_corr_values.index[i][0], color="blue",
                           title=f'Regression Plot (Corr={top_corr_values.iloc[i]:.3f})', corrcoef=top_corr_values.iloc[i])

        update_regplot(ax2_4, data, x=corr_values.index[change_index][1], y=corr_values.index[change_index][0],
                       color="blue",
                       title=f'Regression Plot (Corr={corr_values.iloc[change_index]:.3f})',
                       corrcoef=corr_values.iloc[change_index])
        if changed:
            text.set_text(f'Zmena inciovaná: x={corr_values.index[change_index][1]}, y={corr_values.index[change_index][0]}, '
                               f'Pôvodná hodnota:{old_value:.3f}, Nová hodnota: {corr_values.iloc[change_index]:.3f}, zmena o: {changed:.3f}')

        old_index = change_index
        #po 5% záznamoch sa prepočíta znova percentage_rate(5, len(data-1))
        plt.pause(5)
        text.set_text('')
        ax1.clear()
        for ax2 in reg_ax:
            ax2.clear()
        ax2_4.clear()
        changed = False
