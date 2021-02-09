import time

from main import read_data
import numpy as np
import pandas as pd


def topsis_redirection(type, datas, bestMax=None, bestMin=None):
    newdatas = datas.copy()
    if type == 's':
        print('small to large')
        newdatas = np.max(datas) - datas
    elif type == 'm':
        print('middle to large')
        maxdis = np.max(abs(datas - bestMax))
        newdatas = 1 - abs(datas - bestMax) / maxdis
    elif type == 'r':
        print('range to large')
        maxdis = max(bestMin - np.min(datas), np.max(datas) - bestMax)
        if maxdis <= 0:
            newdatas[newdatas] = 1
        else:
            newdatas = np.where(datas < bestMin, 1 - (bestMin - datas) / maxdis, np.where(datas > bestMax, 1 - (datas - bestMax) / maxdis, 1))
    else:
        print('error type')
    return newdatas


def z_score(datas):
    # print('z score')
    mean = np.mean(datas)
    std = np.std(datas)
    normalizationdatas = (datas - mean) / std
    return normalizationdatas


def min_max(datas):
    # print('min-max')
    min = np.min(datas)
    max = np.max(datas)
    normalizationdatas = (datas - min) / (max - min)
    return normalizationdatas


def topsis_data(file):
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1200)
    td = read_data(file)
    nations = td['Nation']
    td = td.set_index('Nation')
    td['C1'] = td['C1'] / (td['C1'] + 1)
    td['C2'] = td['C2'] / (td['C2'] + 1)
    td = td.dropna(axis=1)
    tarr = td.values

    # redirection
    tarr[:, 2] = topsis_redirection('m', tarr[:, 2], 0.5)           # C1
    tarr[:, 3] = topsis_redirection('m', tarr[:, 3], 0.5)           # C2
    tarr[:, 4] = topsis_redirection('r', tarr[:, 4], 60, 50)        # D1
    tarr[:, 6] = topsis_redirection('m', tarr[:, 6], 30)            # E3
    tarr[:, 8] = topsis_redirection('r', tarr[:, 8], 75, 65)        # F2

    return tarr, nations


def topsis_normalization(arr):
    newarr = np.empty(arr.shape)
    for col in range(0, arr.shape[1]):
        newarr[:, col] = z_score(arr[:, col])
        # newarr[:, col] = min_max(arr[:, col])

    return newarr


def ewm_normalization(ewm_arr1):
    newarr1 = np.empty(ewm_arr1.shape)
    for col in range(0, ewm_arr1.shape[1]):
        # ewm_arr[:, col] = min_max(ewm_arr[:, col])
        # newarr1[:, col] = ewm_arr1[:, col] + 1
        newarr1[:, col] = ewm_arr1[:, col] + 100

    return newarr1


def ewm_probability(ewm_arr2):
    ewm_parr = ewm_arr2.copy()
    for col in range(0, ewm_arr2.shape[1]):
        for row in range(0, ewm_arr2.shape[0]):
            ewm_parr[row, col] = ewm_arr2[row, col] / (ewm_arr2[:, col].sum())

    return ewm_parr


def ewm_entropy(ewm_parr):
    ewm_earr = []
    for col in range(0, ewm_parr.shape[1]):
        summ = 0
        for row in range(0, ewm_parr.shape[0]):
            # print(arr[row, col] * np.log(arr[row, col]))
            # print(arr[row, col])
            print(ewm_parr[row, col], np.log(ewm_parr[row, col]))
            # print(ewm_parr[row, col] * np.log(ewm_parr[row, col]))
            mr = ewm_parr[row, col] * np.log(ewm_parr[row, col])
            summ = summ + mr
            print(mr, summ)
            # print(row, summ)
        entropy = - 1 / np.log(ewm_parr.shape[0]) * summ
        # print(col, entropy)
        ewm_earr.append(entropy)

    print('Entropy:', ewm_earr)

    return ewm_earr


def ewm_weight(listarr):
    ewm_arr4 = np.array(listarr)
    ewm_warr = ewm_arr4 / ewm_arr4.sum()

    print('Weight:', ewm_warr)

    return ewm_warr


def ewm(eeearr):
    newm = ewm_normalization(eeearr)
    pewm = ewm_probability(newm)
    eewm = ewm_entropy(pewm)

    return eewm


def score(dataarr, weight):
    Zmax = np.array([])
    Zmin = np.array([])
    for col in dataarr.T:
        Zmax = np.append(Zmax, np.max(col))
        Zmin = np.append(Zmin, np.min(col))
    print(Zmax, Zmin)
    SList = np.array([])
    for row in dataarr:
        DmaxSquare = 0
        DminSquare = 0
        if not isinstance(row, np.float64):
            for m in range(0, len(row)):
                dmax = np.square(Zmax[m] - row[m])
                DmaxSquare += dmax
                dmin = np.square(Zmin[m] - row[m])
                DminSquare += dmin
            DmaxSquare = weight[m] * DmaxSquare
            DminSquare = weight[m] * DminSquare
            S = np.sqrt(DminSquare) / (np.sqrt(DminSquare) + np.sqrt(DmaxSquare))
            SList = np.append(SList, S)

    return SList


if __name__ == '__main__':
    print('topsis')
    result = pd.DataFrame()
    mean_e = []
    mean_w = []
    if True:
        for year in range(2006, 2020):
            year = str(year)
            file = './data/meanfill/' + year + '_meannation_all.csv'
            tarr, nations = topsis_data(file)
            print(tarr)
            narr = topsis_normalization(tarr)
            # print(narr)
            dataarr = narr

            # ewm
            eewm = ewm(narr)
            mean_e.append(eewm)
            weight = ewm_weight(eewm)
            mean_w.append(list(weight))
            # weight = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]


            # Adatass = narr[:, 0]
            # Aweight = [1]
            # ASList = Adatass
            # # ASList = score(Adatass, Aweight)
            #
            # Bdatass = narr[:, 1]
            # Bweight = [1]
            # BSList = Bdatass
            # # BSList = score(Bdatass, Bweight)
            #
            # Cdatass = narr[:, 2:4]
            # Cweight = ewm(narr[:, 2:4])
            # CSList = score(Cdatass, Cweight)
            #
            # Ddatass = narr[:, 4]
            # Dweight = [1]
            # DSList = Ddatass
            # # DSList = score(Ddatass, Dweight)
            #
            # Edatass = narr[:, 5:8]
            # Eweight = ewm(narr[:, 5:8])
            # ESList = score(Edatass, Eweight)
            #
            # Fdatass = narr[:, 8:10]
            # Fweight = ewm(narr[:, 8:10])
            # FSList = score(Fdatass, Fweight)
            # print(FSList)
            #
            # print(Cweight, Eweight, Fweight)
            #
            # newdataarr = np.empty((dataarr.T).shape)
            # newdataarr[0] = ASList
            # newdataarr[1] = BSList
            # newdataarr[2] = CSList
            # newdataarr[3] = DSList
            # newdataarr[4] = ESList
            # newdataarr[5] = FSList
            #
            # nnewdataarr = newdataarr.T
            # # newdataarr = topsis_normalization(newdataarr)
            # print(ewm(nnewdataarr))
            # newSList = score(nnewdataarr, ewm(nnewdataarr))


            # weight = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
            SList = score(dataarr, weight)

            # result = pd.DataFrame()
            result['Nation'] = nations
            result[year] = SList
            guiyi = result
            guiyi[year] = (guiyi[year] - guiyi[year].min()) / (guiyi[year].max() - guiyi[year].min())
            # time.sleep(5)
            # print(result.sort_values('Score', ascending=False))

            # guiyi = result
            # guiyi['Score'] = (guiyi['Score'] - guiyi['Score'].min()) / (guiyi['Score'].max() - guiyi['Score'].min())
            # print(weight)
            # print(guiyi.sort_values('Score', ascending=False))

            # result.to_excel(writer, sheet_name=year)
        # result.to_csv('./result/ewm_topsis_nake.csv', encoding="utf-8-sig", header=True, index=False)
        print(result)


    all_e = np.array(mean_e)
    all_w = np.array(mean_w)
    mean_e = []
    mean_w = []
    for i in range(0, 10):
        mean_e.append(all_e[:, i].mean())
        mean_w.append(all_w[:, i].mean())

    print(mean_e)
    print(mean_w)
