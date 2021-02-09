import pandas as pd
import os

def read_data(path):
    print('Start reading csv file.')
    data = pd.read_csv(path)
    # print(data)
    return data

def pre_UNESCO():
    pd.set_option('display.max_rows', False)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1200)
    path = './data/UNESCO.csv'
    d = read_data(path)
    qd = d.query('Flags != "Category not applicable"')
    print(qd)
    oqd = qd[(qd.Indicator.str.contains('Students from')) == False]
    # oqd = oqd[(qd.Indicator.str.contains('lower secondary')) == False]
    # oqd = oqd[(qd.Indicator.str.contains('pre-primary')) == False]
    # oqd = oqd[(qd.Indicator.str.contains('primary')) == False]
    # # oqd = oqd[(qd.Indicator.str.contains('secondary')) == False]
    # oqd = oqd[(qd.Indicator.str.contains('upper secondary')) == False]
    # oqd = oqd[(qd.Indicator.str.contains('early childhood')) == False]
    # oqd = oqd[(qd.Indicator.str.contains('Duration')) == False]
    # oqd = oqd[(qd.Indicator.str.contains('Official entrance age')) == False]
    # oqd = oqd[(qd.Indicator.str.contains('female')) == False]
    # oqd = oqd[(qd.Indicator.str.contains('male')) == False]
    # oqd = oqd[(qd.Indicator.str.contains('Outbound')) == False]

    # oqd = oqd[oqd['Indicator'].str.contains('Enrolment in post-secondary non-tertiary education, both sexes') |
    #           oqd['Indicator'].str.contains('Enrolment in tertiary education, all programmes, both sexes')]
    # oqd = oqd[oqd['Indicator'].str.contains('School age population, post-secondary non-tertiary education, both sexes') |
    #           oqd['Indicator'].str.contains('School age population, tertiary education, both sexes')]
    # oqd = oqd[oqd['Indicator'].str.contains('gender parity index') & oqd['Indicator'].str.contains('Gross') |
    #           oqd['Indicator'].str.contains('Enrolment in tertiary education, all programmes, female') |
    #           oqd['Indicator'].str.contains('Enrolment in tertiary education, all programmes, male')]
    # oqd = oqd[oqd['Indicator'].str.contains('Gross graduation ratio from first degree programmes') & oqd['Indicator'].str.contains('both sexes')]
    # oqd = oqd[oqd['Indicator'].str.contains('Net flow ratio of internationally mobile students') |
    #           oqd['Indicator'].str.contains('Percentage of graduates from Science, Technology, Engineering and Mathematics programmes in tertiary education, both sexes')]
    # oqd = oqd[oqd['Indicator'].str.contains('Government expenditure on tertiary education as a percentage of GDP') |
    #           oqd['Indicator'].str.contains('Percentage of graduates from Science, Technology, Engineering and Mathematics programmes in tertiary education, both sexes')]
    # oqd = oqd[oqd['Indicator'].str.contains('Teachers in post-secondary non-tertiary education, both sexes') |
    #           oqd['Indicator'].str.contains('Teachers in tertiary education programmes, both sexes')]
    oqd = oqd[oqd['Indicator'].str.contains('All staff compensation as a percentage of total expenditure in tertiary public institutions') |
              oqd['Indicator'].str.contains('All staff compensation as a percentage of total expenditure in post-secondary non-tertiary public institutions')]

    yoqd = oqd
    # yoqd = oqd.query('Time == 2020 | Time == 2019 | Time == 2018 | Time == 2017 | Time == 2016')
    yoqd = yoqd[['Indicator', 'Country', 'Time', 'Value']]
    print(yoqd)
    yoqd.to_csv('./data/pre/compensation.csv', encoding="utf-8-sig", header=True, index=False)
    pd.set_option('display.max_rows', None)
    # cyoqd = yoqd.query('Country == "China"')
    # print(cyoqd)
    # c = yoqd.Country.value_counts()
    i = yoqd.Indicator.value_counts()
    print(i.sort_index())
    # print(c, '\r', i.sort_index())
    print('END UNESCO')


def pre_data(year):
    file = './data/pre/'
    for root, dirs, files in os.walk(file):

        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list

        # 遍历文件
        for f in files:
            fname = f.split('.')[0]
            fpath = os.path.join(root, f)
            print(fpath)
            if fname:
                if fname[0] != '2':
                    df = read_data(fpath)
                    exec('{} = {}'.format(fname, 'df'))
                    # i = yoqd.Indicator.value_counts()
                    # print(i.sort_index())
                    # exec('print({})'.format(fname))
                    exec('i = {}.Time.value_counts()'.format(fname))
                    exec('q{} = {}.query("Time == {}")'.format(fname, fname, year))
                    exec('print(q{})'.format(fname))
                    exec('q{}.to_csv("./data/pre/time/{}{}.csv", encoding="utf-8-sig", header=True, index=False)'.format(fname, year, fname))


def precob_data(year):
    file = './data/pre/time/'
    for root, dirs, files in os.walk(file):

        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list

        # 遍历文件
        flist = []
        for f in files:
            fname = f.split('.')[0]
            fpath = os.path.join(root, f)
            # print(fpath)
            # print(fname[0:4])
            if fname[0:4] == str(year) and fname[4:]:
                df = read_data(fpath)
                exec('{} = {}'.format(fname[4:], 'df'))
                print(fname[4:])
                # i = yoqd.Indicator.value_counts()
                # print(i.sort_index())
                # exec('print({})'.format(fname))
                # exec('i = {}.Time.value_counts()'.format(fname))
                # exec('q{} = {}.query("Time == {}")'.format(fname, fname, year))
                flist.append(fname[4:])
                # print(str(flist).replace("'", ""))
                newf = str(flist).replace("'", "")
                # exec('print({})'.format(fname[5:]))
                # exec('q{}.to_csv("./data/pre/time/{}{}.csv", encoding="utf-8-sig", header=True, index=False)'.format(fname, year, fname))
            else:
                continue
            exec('result = pd.concat(' + newf + ')')
            exec('print(result)')
            exec('result.to_csv("./data/pre/time/UNESCOtotalByTIme/{}.csv", encoding="utf-8-sig", header=True, index=False)'.format(year))


def nations():
    somec = []
    for year in range(2006, 2020):
        year = str(year)
        # pre_data(year)
        # precob_data(year)
        path = './data/pre/time/UNESCOtotalByTIme/' + year + '.csv'
        df = read_data(path)
        # print(type(df.Country), type(df.Country.value_counts()))
        c = df.Country.value_counts()
        i = df.Indicator.value_counts()
        # print(year+'\r\n', i[i>60], '\r\n' , c[c>=8])
        for ci in list(c[c < 8].index):
            somec.append(ci)
        # print(list(c[c<8].index))
    sc = pd.value_counts(somec)
    # print(list(sc[sc > 10].index))
    # print(len(list(sc[sc <= 10].index)))
    # print(pd.value_counts(list(sc[sc <= 10].index)))
    for year in range(2006, 2020):
        year = str(year)
        # pre_data(year)
        # precob_data(year)
        path = './data/pre/time/UNESCOtotalByTIme/' + year + '.csv'
        df = read_data(path)
        # print(df)
        for nation in list(sc[sc > 10].index):
            newdf = df[df['Country'].str.contains(nation) == False]
            # print(df[df['Country'].str.contains(nation)])
            newdf.to_csv('./data/pre/time/cleanNations/' + year + '.csv',
                         encoding="utf-8-sig", header=True, index=False)

    return list(sc[sc <= 10].index)


def all():
    allindicator = []
    allnation = []
    for year in range(2006, 2020):
        year = str(year)
        # pre_data(year)
        # precob_data(year)
        path = './data/pre/time/cleanNations/' + year + '.csv'
        df = read_data(path)
        # print(type(df.Country), type(df.Country.value_counts()))
        c = df.Country.value_counts()
        i = df.Indicator.value_counts()
        # print(year+'\r\n', i[i>60], '\r\n' , c[c>=8])
        # print(year, len(list(c.index)), len(list(i.index)))
        # print(pd.value_counts(list(i.index)))
        for ii in list(i.index):
            if ii not in allindicator:
                allindicator.append(ii)
        for cc in list(c.index):
            if cc not in allnation:
                allnation.append(cc)

    # print(pd.value_counts(allindicator), len(allindicator))
    return allindicator, allnation


def newformat():
    indicators, nations = all()
    indicators = pd.value_counts(indicators).sort_index().index
    nations = pd.value_counts(nations).sort_index().index
    print(pd.value_counts(indicators).sort_index(), len(indicators))
    print(pd.value_counts(nations).sort_index(), len(nations))
    for year in range(2006, 2020):
        ndf = pd.DataFrame(columns=indicators, index=nations)
        year = str(year)
        path = './data/pre/time/cleanNations/' + year + '.csv'
        df = read_data(path)
        print(df)
        for i in indicators:
            print(i)
            # print(df.query('Indicator=="' + i + '"').sort_values('Country'))
            for c in nations:
                v = df.query('Indicator=="' + i + '"').query('Country=="' + c + '"')['Value']
                if not v.empty:
                    # print(v.iloc[0])
                    ndf.at[c, i] = v.iloc[0]
                # print(list(v.Value)[0])

        print(ndf)
        ndf.to_csv('./data/newformat/' + year + '.csv',
                   encoding="utf-8-sig", header=True, index=True)
    return ndf


def pre_esi():
    esi = read_data('./data/esifull.csv')
    indicators, nations = all()
    print(indicators, nations)
    print(esi.sort_values('f1'))
    esi = esi[['Country', 'Cites/Paper', 'Highly Cited Papers', 'Hot Papers']]
    print(esi)
    cl = []
    ncl = []
    esidf = pd.DataFrame(columns=['Country', 'Cites/Paper', 'Highly Cited Papers', 'Hot Papers', 'Academic Influence'])
    print(esidf)
    for c in nations:
        if not esi.query('Country=="' + c.upper() + '"').empty:
            # print(esi.query('Country=="' + c.upper() + '"'))
            cl.append(c)
            resi = esi.query('Country=="' + c.upper() + '"')
            resi = list(resi.iloc[0])
            esidf = esidf.append(
                [{'Country': c, 'Cites/Paper': resi[1], 'Highly Cited Papers': resi[2], 'Hot Papers': resi[3]}],
                ignore_index=True)
        else:
            if c == 'United States of America':
                if not esi.query('Country=="USA"').empty:
                    print(esi.query('Country=="USA"'))
                    cl.append(c)
                    resi = esi.query('Country=="USA"')
                    resi = list(resi.iloc[0])
                    esidf = esidf.append(
                        [{'Country': c, 'Cites/Paper': resi[1], 'Highly Cited Papers': resi[2], 'Hot Papers': resi[3]}],
                        ignore_index=True)
            elif c == 'China':
                if not esi.query('Country=="CHINA MAINLAND"').empty:
                    print(esi.query('Country=="CHINA MAINLAND"'))
                    cl.append(c)
                    resi = esi.query('Country=="CHINA MAINLAND"')
                    resi = list(resi.iloc[0])
                    esidf = esidf.append(
                        [{'Country': c, 'Cites/Paper': resi[1], 'Highly Cited Papers': resi[2], 'Hot Papers': resi[3]}],
                        ignore_index=True)
            elif c == 'China, Hong Kong Special Administrative Region':
                if not esi.query('Country=="HONG KONG"').empty:
                    print(esi.query('Country=="HONG KONG"'))
                    cl.append(c)
                    resi = esi.query('Country=="HONG KONG"')
                    resi = list(resi.iloc[0])
                    esidf = esidf.append(
                        [{'Country': c, 'Cites/Paper': resi[1], 'Highly Cited Papers': resi[2], 'Hot Papers': resi[3]}],
                        ignore_index=True)
            elif c == 'China, Macao Special Administrative Region':
                if not esi.query('Country=="MACAU"').empty:
                    print(esi.query('Country=="MACAU"'))
                    cl.append(c)
                    resi = esi.query('Country=="MACAU"')
                    resi = list(resi.iloc[0])
                    esidf = esidf.append(
                        [{'Country': c, 'Cites/Paper': resi[1], 'Highly Cited Papers': resi[2], 'Hot Papers': resi[3]}],
                        ignore_index=True)
            elif c == 'Bolivia (Plurinational State of)':
                if not esi.query('Country=="BOLIVIA"').empty:
                    print(esi.query('Country=="BOLIVIA"'))
                    cl.append(c)
                    resi = esi.query('Country=="BOLIVIA"')
                    resi = list(resi.iloc[0])
                    esidf = esidf.append(
                        [{'Country': c, 'Cites/Paper': resi[1], 'Highly Cited Papers': resi[2], 'Hot Papers': resi[3]}],
                        ignore_index=True)
            elif c == 'Congo':
                if not esi.query('Country=="CONGO PEOPLES REP"').empty:
                    print(esi.query('Country=="CONGO PEOPLES REP"'))
                    cl.append(c)
                    resi = esi.query('Country=="CONGO PEOPLES REP"')
                    resi = list(resi.iloc[0])
                    esidf = esidf.append(
                        [{'Country': c, 'Cites/Paper': resi[1], 'Highly Cited Papers': resi[2], 'Hot Papers': resi[3]}],
                        ignore_index=True)
            elif c == 'Democratic Republic of the Congo':
                if not esi.query('Country=="CONGO DEMOCRATIC REPUBLIC"').empty:
                    print(esi.query('Country=="CONGO DEMOCRATIC REPUBLIC"'))
                    cl.append(c)
                    resi = esi.query('Country=="CONGO DEMOCRATIC REPUBLIC"')
                    resi = list(resi.iloc[0])
                    esidf = esidf.append(
                        [{'Country': c, 'Cites/Paper': resi[1], 'Highly Cited Papers': resi[2], 'Hot Papers': resi[3]}],
                        ignore_index=True)
            elif c == 'Dominica':
                if not esi.query('Country=="DOMINICAN REPUBLIC"').empty:
                    print(esi.query('Country=="DOMINICAN REPUBLIC"'))
                    cl.append(c)
                    resi = esi.query('Country=="DOMINICAN REPUBLIC"')
                    resi = list(resi.iloc[0])
                    esidf = esidf.append(
                        [{'Country': c, 'Cites/Paper': resi[1], 'Highly Cited Papers': resi[2], 'Hot Papers': resi[3]}],
                        ignore_index=True)
            elif c == 'Germany':
                if not esi.query('Country=="GERMANY (FED REP GER)"').empty:
                    print(esi.query('Country=="GERMANY (FED REP GER)"'))
                    cl.append(c)
                    resi = esi.query('Country=="GERMANY (FED REP GER)"')
                    resi = list(resi.iloc[0])
                    esidf = esidf.append(
                        [{'Country': c, 'Cites/Paper': resi[1], 'Highly Cited Papers': resi[2], 'Hot Papers': resi[3]}],
                        ignore_index=True)
            elif c == 'Lao People\'s Democratic Republic':
                if not esi.query('Country=="LAOS"').empty:
                    print(esi.query('Country=="LAOS"'))
                    cl.append(c)
                    resi = esi.query('Country=="LAOS"')
                    resi = list(resi.iloc[0])
                    esidf = esidf.append(
                        [{'Country': c, 'Cites/Paper': resi[1], 'Highly Cited Papers': resi[2], 'Hot Papers': resi[3]}],
                        ignore_index=True)
            elif c == 'Republic of Moldova':
                if not esi.query('Country=="MOLDOVA"').empty:
                    print(esi.query('Country=="MOLDOVA"'))
                    cl.append(c)
                    resi = esi.query('Country=="MOLDOVA"')
                    resi = list(resi.iloc[0])
                    esidf = esidf.append(
                        [{'Country': c, 'Cites/Paper': resi[1], 'Highly Cited Papers': resi[2], 'Hot Papers': resi[3]}],
                        ignore_index=True)
            elif c == 'Russian Federation':
                if not esi.query('Country=="RUSSIA"').empty:
                    print(esi.query('Country=="RUSSIA"'))
                    cl.append(c)
                    resi = esi.query('Country=="RUSSIA"')
                    resi = list(resi.iloc[0])
                    esidf = esidf.append(
                        [{'Country': c, 'Cites/Paper': resi[1], 'Highly Cited Papers': resi[2], 'Hot Papers': resi[3]}],
                        ignore_index=True)
            elif c == 'Iran (Islamic Republic of)':
                if not esi.query('Country=="IRAN"').empty:
                    print(esi.query('Country=="IRAN"'))
                    cl.append(c)
                    resi = esi.query('Country=="IRAN"')
                    resi = list(resi.iloc[0])
                    esidf = esidf.append(
                        [{'Country': c, 'Cites/Paper': resi[1], 'Highly Cited Papers': resi[2], 'Hot Papers': resi[3]}],
                        ignore_index=True)
            elif c == 'Georgia':
                if not esi.query('Country=="REPUBLIC OF GEORGIA"').empty:
                    print(esi.query('Country=="REPUBLIC OF GEORGIA"'))
                    cl.append(c)
                    resi = esi.query('Country=="REPUBLIC OF GEORGIA"')
                    resi = list(resi.iloc[0])
                    esidf = esidf.append(
                        [{'Country': c, 'Cites/Paper': resi[1], 'Highly Cited Papers': resi[2], 'Hot Papers': resi[3]}],
                        ignore_index=True)
            elif c == 'Brunei Darussalam':
                if not esi.query('Country=="BRUNEI"').empty:
                    print(esi.query('Country=="BRUNEI"'))
                    cl.append(c)
                    resi = esi.query('Country=="BRUNEI"')
                    resi = list(resi.iloc[0])
                    esidf = esidf.append(
                        [{'Country': c, 'Cites/Paper': resi[1], 'Highly Cited Papers': resi[2], 'Hot Papers': resi[3]}],
                        ignore_index=True)
            elif c == 'Bosnia and Herzegovina':
                if not esi.query('Country=="BOSNIA & HERZEGOVINA"').empty:
                    print(esi.query('Country=="BOSNIA & HERZEGOVINA"'))
                    cl.append(c)
                    resi = esi.query('Country=="BOSNIA & HERZEGOVINA"')
                    resi = list(resi.iloc[0])
                    esidf = esidf.append(
                        [{'Country': c, 'Cites/Paper': resi[1], 'Highly Cited Papers': resi[2], 'Hot Papers': resi[3]}],
                        ignore_index=True)
            elif c == 'Republic of Korea':
                if not esi.query('Country=="SOUTH KOREA"').empty:
                    print(esi.query('Country=="SOUTH KOREA"'))
                    cl.append(c)
                    resi = esi.query('Country=="SOUTH KOREA"')
                    resi = list(resi.iloc[0])
                    esidf = esidf.append(
                        [{'Country': c, 'Cites/Paper': resi[1], 'Highly Cited Papers': resi[2], 'Hot Papers': resi[3]}],
                        ignore_index=True)
            elif c == 'United Republic of Tanzania':
                if not esi.query('Country=="TANZANIA"').empty:
                    print(esi.query('Country=="TANZANIA"'))
                    cl.append(c)
                    resi = esi.query('Country=="TANZANIA"')
                    resi = list(resi.iloc[0])
                    esidf = esidf.append(
                        [{'Country': c, 'Cites/Paper': resi[1], 'Highly Cited Papers': resi[2], 'Hot Papers': resi[3]}],
                        ignore_index=True)
            elif c == 'Venezuela (Bolivarian Republic of)':
                if not esi.query('Country=="VENEZUELA"').empty:
                    print(esi.query('Country=="VENEZUELA"'))
                    cl.append(c)
                    resi = esi.query('Country=="VENEZUELA"')
                    resi = list(resi.iloc[0])
                    esidf = esidf.append(
                        [{'Country': c, 'Cites/Paper': resi[1], 'Highly Cited Papers': resi[2], 'Hot Papers': resi[3]}],
                        ignore_index=True)
            elif c == 'Viet Nam':
                if not esi.query('Country=="VIETNAM"').empty:
                    print(esi.query('Country=="VIETNAM"'))
                    cl.append(c)
                    resi = esi.query('Country=="VIETNAM"')
                    resi = list(resi.iloc[0])
                    esidf = esidf.append(
                        [{'Country': c, 'Cites/Paper': resi[1], 'Highly Cited Papers': resi[2], 'Hot Papers': resi[3]}],
                        ignore_index=True)
            elif c == 'United Kingdom of Great Britain and Northern Ireland':
                if not esi.query('Country=="ENGLAND"').empty:
                    print(esi.query('Country=="ENGLAND"'))
                    cl.append(c)
                    resi = esi.query('Country=="ENGLAND"')
                    resi = list(resi.iloc[0])
                    esidf = esidf.append(
                        [{'Country': c, 'Cites/Paper': resi[1], 'Highly Cited Papers': resi[2], 'Hot Papers': resi[3]}],
                        ignore_index=True)
            else:
                ncl.append(c)
    pd.set_option('display.max_rows', None)
    print(esidf)
    esidf.to_csv('./data/esi/esi_noaf.csv', encoding="utf-8-sig", header=True, index=False)
    # print(pd.value_counts(cl).sort_index(), len(cl))
    print(pd.value_counts(ncl).sort_index(), len(ncl))


if __name__ == '__main__':
    # pre_UNESCO()
    # pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1200)
    # pd.set_option('display.max_colwidth', 400)
    # pre_UNESCO()
    # for year in range(2006, 2020):
    #     pre_data(year)
    # for year in range(2006, 2020):
    #     precob_data(year)
    # nations()
    newformat()