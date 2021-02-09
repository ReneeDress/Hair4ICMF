from main import read_data
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def academicinfluence(path):
    print('Calculating Academic Influence...')
    noaf = read_data(path)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1200)
    # pd.set_option('display.max_colwidth', 400)
    # print(noaf)
    noaf = noaf.apply(lambda x: x.replace(0, 1))
    noaf['Academic Influence'] = noaf['Cites/Paper'] * (np.log(noaf['Highly Cited Papers'] * noaf['Hot Papers']) / np.log(100))
    # print(noaf.sort_values(by='Academic Influence', ascending=False))
    af = noaf
    af.rename(columns={'Country': 'Nation'}, inplace=True)
    print(af)
    return af


if __name__ == '__main__':
    print('Start')
    file = './data/esi/esi_noaf.csv'
    af = academicinfluence(file)[['Cites/Paper', 'Highly Cited Papers', 'Hot Papers','Academic Influence'
                                  ]]
    for col in ['Cites/Paper', 'Highly Cited Papers', 'Hot Papers', 'Academic Influence']:
        af[col] = (af[col] - af[col].min()) / (af[col].max() - af[col].min())
    af.plot(xlabel='Nations\' Number', ylabel='Normalized Value', figsize=(11, 3))
    plt.title('The Academic Influence Model - Inputs')
    plt.show()