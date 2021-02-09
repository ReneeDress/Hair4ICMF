from main import read_data
import pandas as pd
import numpy as np
from plot import show
import matplotlib.pyplot as plt


if __name__ == '__main__':
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1200)
    # pd.set_option('display.max_colwidth', 400)
    ndf = read_data('./data/allfill/2019_fill_all.csv')
    mdf = read_data('./data/meanfill/2019_meannation_all.csv')
    mdf.dropna(axis=1, inplace=True)
    mdf = mdf.append(mdf.query('Nation == "Poland"'), ignore_index=True)
    mdf.iloc[124, 0] = 'Poland - New Data'
    print(mdf)
    mdf.set_index('Nation', inplace=True)

    print(mdf.at['Poland', 'B1'], mdf.at['Poland', 'C1'], mdf.at['Poland', 'E2'], mdf.at['Poland', 'F1'])
    # mdf = mdf.append(mdf.loc['Poland'])
    # print(mdf)
    mdf.at['Poland - New Data', 'B1'] = 10
    mdf.at['Poland - New Data', 'C1'] = 1.1
    mdf.at['Poland - New Data', 'E2'] = 17
    mdf.at['Poland - New Data', 'F1'] = 1.6

    mdf['C1'] = mdf['C1'] / (mdf['C1'] + 1)
    mdf['C2'] = mdf['C2'] / (mdf['C2'] + 1)

    maxdis = np.max(abs(mdf['C1'] - 0.5))
    mdf['C1'] = 1 - abs(mdf['C1'] - 0.5) / maxdis

    maxdis = np.max(abs(mdf['C2'] - 0.5))
    mdf['C2'] = 1 - abs(mdf['C2'] - 0.5) / maxdis

    maxdis = np.max(abs(mdf['E3'] - 30))
    mdf['E3'] = 1 - abs(mdf['E3'] - 30) / maxdis

    bestMin = 50
    bestMax = 60
    maxdis = max(bestMin - np.min(mdf['D1']), np.max(mdf['D1']) - bestMax)
    if maxdis <= 0:
        mdf['D1'][mdf['D1']] = 1
    else:
        mdf['D1'] = np.where(mdf['D1'] < bestMin, 1 - (bestMin - mdf['D1']) / maxdis,
                            np.where(mdf['D1'] > bestMax, 1 - (mdf['D1'] - bestMax) / maxdis, 1))

    bestMin = 65
    bestMax = 75
    maxdis = max(bestMin - np.min(mdf['F2']), np.max(mdf['F2']) - bestMax)
    if maxdis <= 0:
        mdf['F2'][mdf['F2']] = 1
    else:
        mdf['F2'] = np.where(mdf['F2'] < bestMin, 1 - (bestMin - mdf['F2']) / maxdis,
                            np.where(mdf['F2'] > bestMax, 1 - (mdf['F2'] - bestMax) / maxdis, 1))

    mdf['A1'] = (mdf['A1'] - np.min(mdf['A1'])) / (np.max(mdf['A1']) - np.min(mdf['A1']))
    mdf['B1'] = (mdf['B1'] - np.min(mdf['B1'])) / (np.max(mdf['B1']) - np.min(mdf['B1']))
    mdf['C1'] = (mdf['C1'] - np.min(mdf['C1'])) / (np.max(mdf['C1']) - np.min(mdf['C1']))
    mdf['C2'] = (mdf['C2'] - np.min(mdf['C2'])) / (np.max(mdf['C2']) - np.min(mdf['C2']))
    mdf['D1'] = (mdf['D1'] - np.min(mdf['D1'])) / (np.max(mdf['D1']) - np.min(mdf['D1']))
    mdf['E1'] = (mdf['E1'] - np.min(mdf['E1'])) / (np.max(mdf['E1']) - np.min(mdf['E1']))
    mdf['E2'] = (mdf['E2'] - np.min(mdf['E2'])) / (np.max(mdf['E2']) - np.min(mdf['E2']))
    mdf['E3'] = (mdf['E3'] - np.min(mdf['E3'])) / (np.max(mdf['E3']) - np.min(mdf['E3']))
    mdf['F1'] = (mdf['F1'] - np.min(mdf['F1'])) / (np.max(mdf['F1']) - np.min(mdf['F1']))
    mdf['F2'] = (mdf['F2'] - np.min(mdf['F2'])) / (np.max(mdf['F2']) - np.min(mdf['F2']))

    print(mdf.at['Poland', 'B1'], mdf.at['Poland', 'C1'], mdf.at['Poland', 'E2'], mdf.at['Poland', 'F1'])

    mdfT = (mdf.copy()).T
    mdfT.reset_index()
    mdfT['MEAN'] = mdfT.apply(lambda x: x.mean(), axis=1)
    target = mdfT[['Poland', 'Germany', 'MEAN', 'Poland - New Data']]
    target.plot(xlabel='Indicators', figsize=(15, 3))
    # plt.title('Normal TOPSIS apply to 6 selected nations (Normalization)')
    # plt.title('TOPSIS with EWM apply to 6 selected nations (Non-Normalization)')
    plt.title('Comparision between Poland, Germany, and MEAN (Normalization)')
    # num1, num2, num3, num4 = 3, 0, 3, 0
    # plt.legend(bbox_to_anchor=(num1, num2), loc=num3, borderaxespad=num4)
    plt.show()
    print(target)
    print(target.at['B1', 'Poland'])