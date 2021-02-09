from main import read_data
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def show(df):
    df.plot()
    # plt.title('Normal TOPSIS apply to 6 selected nations (Non-Normalization)')
    # plt.title('TOPSIS with EWM apply to 6 selected nations (Non-Normalization)')
    plt.title('TOPSIS with EWM apply to All nations (Non-Normalization)')
    num1, num2, num3, num4 = 3, 0, 3, 0
    plt.legend(bbox_to_anchor=(num1, num2), loc=num3, borderaxespad=num4)
    plt.show()


if __name__ == '__main__':
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1200)
    # pd.set_option('display.max_colwidth', 400)
    nt1 = read_data('./result/csv_zscore/normal_topsis_nake.csv')
    # print(nt1)
    nt1.set_index('Nation', inplace=True)
    # print(nt1)
    nt1T = nt1.T
    nt1T.reset_index()
    nt1T['MEAN'] = nt1T.apply(lambda x: x.mean(), axis=1)
    # nt1T.columns = nt1T[:, 1]
    print(nt1T)
    # show(nt1T[['Germany', 'Poland', 'Ethiopia', 'Switzerland', 'Romania', 'MEAN']])
    show(nt1T)
