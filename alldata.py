from main import read_data
from academicinfluence import academicinfluence
import numpy as np
import pandas as pd


def unesco(path, nations, academic):
    for year in range(2006, 2020):
        year = str(year)
        file = path + year + '.csv'
        udf = read_data(file)
        udf['Teachers in higher education, both sexes (number)'] \
            = udf['Teachers in post-secondary non-tertiary education, both sexes (number)'] \
              + udf['Teachers in tertiary education programmes, both sexes (number)']
        udf['Enrolment in higher education, both sexes (number)'] \
            = udf['Enrolment in post-secondary non-tertiary education, both sexes (number)'] \
              + udf['Enrolment in tertiary education, all programmes, both sexes (number)']
        udf['Teacher-to-Student ratio in higher education (number per 100 students)'] = udf['Teachers in higher education, both sexes (number)'] / udf['Enrolment in higher education, both sexes (number)'] * 100
        # print(udf[['Unnamed: 0', 'Teacher-to-Student ratio in higher education (number per 100 students)']])
        udf['School age population, higher education, both sexes (number)'] \
            = udf['School age population, post-secondary non-tertiary education, both sexes (number)'] \
              + udf['School age population, tertiary education, both sexes (number)']
        udf['Enrolment to school age population ratio in higher education, both sexes (%)'] = udf['Enrolment in higher education, both sexes (number)'] / udf['School age population, higher education, both sexes (number)']
        # print(udf[['Unnamed: 0', 'Enrolment to school age population ratio in higher education, both sexes (%)']])
        udf['Enrolment in higher education, all programmes, gender parity index (GPI)'] \
            = (udf['Enrolment in tertiary education, all programmes, female (number)']
               / udf['Enrolment in tertiary education, all programmes, male (number)'])
        udf['All staff compensation as a percentage of total expenditure in higher public institutions (%)'] \
            = (udf['All staff compensation as a percentage of total expenditure in post-secondary non-tertiary public institutions (%)'] + udf['All staff compensation as a percentage of total expenditure in tertiary public institutions (%)']) / 2
        # print(udf[['Unnamed: 0', 'Enrolment in higher education, all programmes, gender parity index (GPI)']])
        cols = ['Nation',
                'Enrolment to school age population ratio in higher education, both sexes (%)',
                'Number of tertiary education institutions per thousand population (number per thousand population)',
                'Teacher-to-Student ratio in higher education (number per 100 students)',
                'Mean tuition of public institution on tertiary education as a percentage of average family consumption (%)',
                'Enrolment in higher education, all programmes, gender parity index (GPI)',
                'Gross graduation ratio from first degree programmes (ISCED 6 and 7) in tertiary education, gender parity index (GPI)',
                'Differences of distribution in higher education (score)',
                'Gross graduation ratio from first degree programmes (ISCED 6 and 7) in tertiary education, both sexes (%)',
                'Suitability between higher education and employment market (score)',
                'Net flow ratio of internationally mobile students (inbound - outbound), both sexes (%)',
                'Academic Influence (score)',
                'Percentage of graduates from Science, Technology, Engineering and Mathematics programmes in tertiary education, both sexes (%)',
                'Government expenditure on tertiary education as a percentage of GDP (%)',
                'All staff compensation as a percentage of total expenditure in higher public institutions (%)']
        cols = ['Nation',
                'A1',
                'A2',
                'B1',
                'B2',
                'C1',
                'C2',
                'C3',
                'D1',
                'D2',
                'E1',
                'E2',
                'E3',
                'F1',
                'F2']
        udf = udf[['Unnamed: 0',
                'Enrolment to school age population ratio in higher education, both sexes (%)',
                'Teacher-to-Student ratio in higher education (number per 100 students)',
                'Enrolment in higher education, all programmes, gender parity index (GPI)',
                'Gross graduation ratio from first degree programmes (ISCED 6 and 7) in tertiary education, gender parity index (GPI)',
                'Gross graduation ratio from first degree programmes (ISCED 6 and 7) in tertiary education, both sexes (%)',
                'Net flow ratio of internationally mobile students (inbound - outbound), both sexes (%)',
                'Percentage of graduates from Science, Technology, Engineering and Mathematics programmes in tertiary education, both sexes (%)',
                'Government expenditure on tertiary education as a percentage of GDP (%)',
                'All staff compensation as a percentage of total expenditure in higher public institutions (%)']]
        # print(udf)
        udf.rename(columns={'Unnamed: 0': 'Nation'}, inplace=True)
        # cols.extend(list(udf.columns)[1:])
        # print(pd.value_counts(list(udf.columns)[0:]).sort_index())
        nudf = pd.DataFrame(columns=cols)
        for na in nations:
            na = str(na)
            rn = udf.query('Nation =="' + na + '"')
            af = academic.query('Nation =="' + na + '"')
            if not rn.empty:
                rn = list(rn.iloc[0])
                af = list(af.iloc[0])[1]
                nudf = nudf.append({
                    'Nation': na,
                    'A1': rn[1],
                    'B1': rn[2],
                    'C1': rn[3],
                    'C2': rn[4],
                    'D1': rn[5],
                    'E1': rn[6],
                    'E2': af,
                    'E3': rn[7],
                    'F1': rn[8],
                    'F2': rn[9]}, ignore_index=True)
                # nudf = nudf.append({
                #     'Nation': na,
                #     'Enrolment to school age population ratio in higher education, both sexes (%)': rn[1],
                #     # 'Number of tertiary education institutions per thousand population (number per thousand population)',
                #     'Teacher-to-Student ratio in higher education (number per 100 students)': rn[2],
                #     # 'Mean tuition of public institution on tertiary education as a percentage of average family consumption (%)',
                #     'Enrolment in higher education, all programmes, gender parity index (GPI)': rn[3],
                #     'Gross graduation ratio from first degree programmes (ISCED 6 and 7) in tertiary education, gender parity index (GPI)': rn[4],
                #     'Gross graduation ratio from first degree programmes (ISCED 6 and 7) in tertiary education, both sexes (%)': rn[5],
                #     'Net flow ratio of internationally mobile students (inbound - outbound), both sexes (%)': rn[6],
                #     'Academic Influence (score)': af,
                #     'Percentage of graduates from Science, Technology, Engineering and Mathematics programmes in tertiary education, both sexes (%)': rn[7],
                #     'Government expenditure on tertiary education as a percentage of GDP (%)': rn[8],
                #     'All staff compensation as a percentage of total expenditure in higher public institutions (%)': rn[9]}, ignore_index=True)
        print(year)
        print(nudf)
        exec('nudf.to_csv(\'./data/all/{}_nake_all.csv\', encoding="utf-8-sig", header=True, index=False)'.format(year))


if __name__ == '__main__':
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1200)
    # pd.set_option('display.max_colwidth', 400)

    # to all
    # print('Preparing data...')
    # unesco_path = './data/newformat/'
    # af_path = './data/esi/esi_noaf.csv'
    # af = academicinfluence(af_path)
    # # print(af[['Nation', 'Academic Influence']])
    # nations = af['Nation']
    # nations = list(nations)
    # # print(nations)
    # unesco(unesco_path, nations, af)

    # # data fill by year
    # for year in range(2007, 2020):
    #     pvyr = str(year - 1)
    #     cryr = str(year)
    #     prev = read_data('./data/allfill/' + pvyr + '_fill_all.csv')
    #     curr = read_data('./data/all/' + cryr + '_nake_all.csv')
    #     # print(curr)
    #     curr = curr.combine_first(prev)
    #     # print(prev)
    #     print(curr)
    #     curr.to_csv('./data/allfill/' + cryr + '_fill_all.csv', encoding="utf-8-sig", header=True, index=False)
    #
    # # nation selection
    # latest = read_data('./data/allfill/2019_fill_all.csv')
    # # print(latest[['Nation', 'A1', 'B1', 'C1', 'C2', 'D1', 'E1', 'E2', 'E3', 'F1', 'F2']])
    # nlatest = latest[['Nation', 'A1', 'B1', 'C1', 'C2', 'D1', 'E1', 'E2', 'E3', 'F1', 'F2']]
    # nlatest = (nlatest.dropna(axis=0, thresh=5)).reset_index(drop = True)
    # newnations = list(nlatest['Nation'])
    # print(newnations)
    #
    # for year in range(2006, 2020):
    #     year = str(year)
    #     old = read_data('./data/allfill/' + year + '_fill_all.csv')
    #     new = pd.DataFrame(columns=old.columns)
    #     for nn in newnations:
    #         if not old.query('Nation == "' + nn + '"').empty:
    #             # print(old.query('Nation == "' + nn + '"'))
    #             new = new.append(old.query('Nation == "' + nn + '"'), ignore_index=True)
    #     print(new)
    #     new.to_csv('./data/nationall/' + year + '_nation_all.csv', encoding="utf-8-sig", header=True, index=False)


    # data fill by mean
    for year in range(2006, 2020):
        year = str(year)
        datas = read_data('./data/nationall/' + year + '_nation_all.csv')
        for column in list(datas.columns[datas.isnull().sum() > 0]):
            mean_val = datas[column].mean()
            datas[column].fillna(mean_val, inplace=True)
        print(datas)
        datas.to_csv('./data/meanfill/' + year + '_meannation_all.csv', encoding="utf-8-sig", header=True, index=False)