import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.gridspec import GridSpec

#metoda pre precitanie dát z csv suboru
def read_data():
    data = pd.read_csv("../data/new_data.csv", delimiter=';', on_bad_lines='skip')
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
                line_kws={'color': 'red', 'linewidth': 1}, scatter_kws={'s': 5}, fit_reg=True)
    ax.set_title(title)


if __name__ == "__main__":
    plt.ion()
    obrazok = 250
    corr_data = None
    data, corr_data = read_data()
    matrix = np.triu(corr_data)

    # Create a 2x4 grid of subplots
    fig = plt.figure(figsize=(13, 6))
    gs = GridSpec(2, 4, figure=fig)

    ax1 = fig.add_subplot(gs[0:2, 0:2])  # Spanning 2 rows and 2 columns

    ax2_1 = fig.add_subplot(gs[0, 2])  # 1st row, 1st column
    ax2_2 = fig.add_subplot(gs[0, 3])  # 1st row, 2nd column
    ax2_3 = fig.add_subplot(gs[1, 2])  # 2nd row, 1st column
    ax2_4 = fig.add_subplot(gs[1, 3])  # 2nd row, 2nd column

    plt.subplots_adjust(wspace=0.4, hspace=0.6)

    #heatmap init
    sns.heatmap(corr_data, ax=ax1, cbar=True, annot=True,
                annot_kws={'size': 8}, fmt=".2f", mask=matrix, cmap='coolwarm', vmin=-1, vmax=1)

    while True:
        #data, corr_data = recalculate()

        # odstranenie duplikatov a diagonaly, nastavenie na NaN
        # zoradenie od najvacsieho po najmensie .abs() zaruci aj antikorelaciu
        # top_corr_values je v tvare (y,x,hodnota) vyberam prve styri
        corr_values = corr_data.where(np.triu(np.ones(corr_data.shape), k=1).astype(bool)).unstack()
        sorted_corr_values = corr_values.abs().sort_values(ascending=False)
        top_corr_values = sorted_corr_values.iloc[0:4]

        update_heatmap(ax1, corr_data, matrix, 'Correlation Heatmap')

        # top_corr_values.index[0][0] hodnota y
        # top_corr_values.index[0][1] hodnota x
        # top_corr_values.iloc[0] hodnota korelacie
        # print(top_corr_values.index[0][0], top_corr_values.index[0][1], top_corr_values.iloc[0])
        reg_ax = [ax2_1, ax2_2, ax2_3, ax2_4]
        for i in range(0, 4):
            update_regplot(reg_ax[i], data, x=top_corr_values.index[i][1], y=top_corr_values.index[i][0], color="black",
                           title=f'Regression Plot (Corr={top_corr_values.iloc[i]:.3f})', corrcoef=top_corr_values.iloc[i])

        #plt.savefig(f'../pictures/time/time{obrazok}.png', dpi=600)
        plt.pause(10)
        obrazok += 1
        ax1.clear()
        for ax2 in reg_ax:
            ax2.clear()