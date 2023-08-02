import csv

full_longt = 21600  # 以分计的全球经度，在赤道上，一分约为 1.855 公里
half_longt = 10800  # 以分计的半球经度，用于计算经度差绝对值，当两个经度差diff大于 10800 时，实际经度差是 21600-diff
full_latit = 10800  # 以分计的全球纬度，一分约为 1.855 公里
pdir = '../downloads/NMDIS/'

# 原始数据的数项分割长度
s_len = [10, 6, 8, 4, 2, 2, 2, 2, 2, 1,
         5, 2, 2, 5, 1, 3, 2, 5, 1, 1,
         1, 3, 1, 4, 1, 6, 1, 5, 1, 3,
         1, 4, 1, 3, 1, 5, 1, 6, 1, 4,
         1, 4, 1, 2, 1, 1, 2, 1, 1, 20,
         1, 2, 1, 5, 1, 2, 1, 5, 1, 2,
         1, 5, 1, 5, 1, 2, 1, 1, 1, 1,
         1, 6, 1, 1]


# 检查"海洋气象综合数据集"的字典
check_dict = {
    '2': '      ',
    '3': '        ',
    '11': ' 0000',
    '22': '-99',
    '24': '-9.9',
    '26': '-999.9',  # slp, 海平面气压
    '28': '-99.9', # at, 气温
    '30': '-99', # hr, relative humidity 相对湿度
    '32': '-9.9',
    '34': '-99',
    '36': '-99.9',
    '38': '-99.9 ', # sst, sea surface temperature
    '40': '-9.9',
    '42': '-9.9',
    '44': ' /',
    '46': 'j',
    '49': 'j',
    '50': '                    ',
    '52': ' /',
    '54': '     ',
    '56': ' /',
    '58': '     ',
    '60': ' /',
    '62': ' -999',
    '64': '     ',
    '66': '//',
    '68': ' ',
    '70': ' ',
    '72': '-999.9',
    '73': ' ',
}


def convert(file_name):
    """
    convert origin data into comma seperated lines without headline and save in .CSV file

    :param file_name: file name without the .DAT appendix
    """
    file = open(pdir+file_name+'.DAT', 'r')

    s_list = []
    i = 0
    for line in file:
        i += 1
        s_list.append(line)

    split_list = ['1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74']
    for line in s_list:
        item = []
        for i in range(len(s_len)):
            cur_pos = sum(s_len[:i])
            item.append(line[cur_pos:cur_pos+s_len[i]])
        split_list.append(','.join(item))

    with open(pdir + file_name + '.CSV', 'w') as f:
        for line in split_list:
            f.write(f"{line}\n")

    print('convert done. total lines:' + str(len(split_list)))


def check(file_name):
    """
    check the efficient of data using the check dict
    :param file_name: the file name without parent dir or '.CSV' appendix
    :return:
    """
    f = open(pdir+file_name+'.CSV', mode="r")
    reader = csv.DictReader(f)
    count_dict = {}
    i = 0
    for row in reader:
        i += 1
        for k in check_dict:
            if row[k] != check_dict[k]:
                '''
                if k=='34':
                    print(k, ',', row[k], ',', len(row[k]), ',', check_dict[k], ',', len(check_dict[k]))
                '''
                if k in count_dict:
                    count_dict[k] += 1
                else:
                    count_dict[k] = 1
        '''
        if i >= 1000:
            exit(0)
        '''
    print('check done. total rows:', i)
    for k in count_dict:
        count_dict[k] = round(count_dict[k]/i, 2)
    return count_dict


def extract_sst(file_name):
    """
    extract data mainly about sst
    :param file_name: the file name without parent dir or '.CSV' appendix
    :return: None
    """
    f = open(pdir+file_name+'.CSV', mode="r")
    reader = csv.DictReader(f)
    filtered_list = ['timeh,latit,longt,slp,at,rh,sst']
    row_num = 0
    for row in reader:
        row_num += 1
        # 预处理
        row['15'] = row['15'].upper()
        row['19'] = row['19'].upper()

        # 筛选有效数据
        if not (row['15'] in ['N', 'S'] and row['19'] in ['E', 'W']):
            continue
        skip_row = False
        for k in ['26', '28', '30', '38']:  # 海平面气压，气温，相对湿度，sst
            if row[k] == check_dict[k]:
                skip_row = True
                break
        if skip_row:
            continue

        # 时间，记录到小时
        timeh = row['4'] + row['5'] + row['6'] + row['7']
        # 纬度，以分为单位，即 度*60+分; N为正，S为负
        latit = int(row['12']) * 60 + int(row['13'])
        latit = latit if row['15'] == 'N' else -latit
        # 经度，以分为单位，即 度*60+分; 这里以东经为准，西经换成东经表示
        longt = int(row['16']) * 60 + int(row['17'])
        longt = longt if row['19'] == 'E' else (21600 - longt)

        filtered_list.append(','.join([str(timeh), str(latit), str(longt), row['26'].strip(' '),
                                       row['28'].strip(' '), row['30'].strip(' '), row['38'].strip(' ')]))

    print("extract sst done. %d items found." % len(filtered_list))
    with open(pdir + file_name + '_sst.CSV', 'w') as f:
        for line in filtered_list:
            f.write(f"{line}\n")


file_name = 'S1500-Y2018-SSM'
# print(check(file_name))
convert(file_name)
extract_sst(file_name)