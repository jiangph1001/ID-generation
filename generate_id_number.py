# -*- coding:utf-8

import datetime,argparse,csv

# 获取身份证号码最后一位
# 根据前17位进行计算
# Parameter：
#   id:前17位的字符串列表
def get_lastnumber(id):
    weight=[7,9,10,5,8,4,2,1,6,3,7,9,10,5,8,4,2]
    if len(weight) != len(id):
        print("计算最后一位时出错!")
        return 0
    sum = 0
    for i in range(len(weight)):
        sum = sum + weight[i] * int(id[i]) 
    loc = sum % 11
    ans="10X98765432"
    return ans[loc]

# 将Datetime格式转换成字符串格式并输出
def get_birthday_str(dt):
    birth = dt.strftime("%Y%m%d")
    return birth

# 输入年月日的信息，输出Datetime格式
def convert_datatime(year,month,day):
    if isinstance(year,str):
        year = int(year)
    if isinstance(month,str):
        month = int(month)
    if isinstance(day,str):
        day = int(day)
    return datetime.datetime(year,month,day)

# 根据初始日期和截止日期生成字符串列表
def generate_bithday_by_range(begin_dt,end_dt):
    dt = begin_dt
    birthday=[]
    while dt <= end_dt:
        birthday.append(get_birthday_str(dt))
        dt = dt + datetime.timedelta(days=1)
    return birthday


def get_prefix_by_provice(province):
    return get_prefix(3,province)

def get_prefix_by_area(area):
    return get_prefix(1,area)

def get_prefix_by_city(city):
    num = get_prefix(1,city)
    return get_prefix(0,num[0][:4])

# 获取前缀
def get_prefix(mode,arg_str):
    file_name = "prefix.csv"
    prefix6 = []
    with open(file_name,'r') as fd:
        csv_reader = csv.reader(fd)
        for row in csv_reader:
            if arg_str in row[mode]:
                prefix6.append(row[0])
    return prefix6

# 获取所有的生日字符串
# Parameter:
#   date_str: 日期字符串
def get_all_birthday(date_str):
    date_str = date_str.split('-')
    if len(date_str) == 2:
        # 两个日期的情况，输出这之间的字符串
        begin_date = date_str[0].split('/')
        end_date = date_str[1].split('/')
        begin_dt = convert_datatime(begin_date[0],begin_date[1],begin_date[2])
        end_dt = convert_datatime(end_date[0],end_date[1],end_date[2])
        birthday = generate_bithday_by_range(begin_dt,end_dt)
    else:
        # 一个日期，直接输出当天的字符串
        date = date_str[0].split('/')
        dt=convert_datatime(date[0],date[1],date[2])
        birthday = []
        birthday.append(get_birthday_str(dt))
    return birthday


if __name__ == "__main__":

    gender_dict = {"女":"02468","男":"13579"} # female：0  male:1
    parser = argparse.ArgumentParser()
    parser.add_argument("-g","--gender",default = "男",help="性别，女或男")
    parser.add_argument("-o","--output",help="输出到文件")
    parser.add_argument("-d","--date",default="1970/01/01",help="出生日期（年/月/日）,例：1970/1/1。范围:1970/01/01-1998/02/02")
    # parser.add_argument("-r","--random",help="三位随机码")
    parser.add_argument("-p","--province",default='北京市',help="出生地址精确到省/直辖市")
    parser.add_argument("-c","--city",help="出生地址精确到地级市")
    parser.add_argument("-a","--area",help="出生地址精确到县级市")
    args = parser.parse_args()

    gender = args.gender
    birthday = get_all_birthday(args.date)
    
    if args.area:
        prefix6 = get_prefix_by_area(args.area)
    elif args.city:
        prefix6 = get_prefix_by_city(args.city)
    elif args.province:
        prefix6 = get_prefix_by_provice(args.province)

    if args.output:
        fd = open(args.output,"w")    
    for pre in prefix6:
        for date in birthday:
            for num in range(100):
                for gender_code in gender_dict[gender]:
                    id = pre + date + str(num).zfill(2) + gender_code
                    id = id + get_lastnumber(id)
                    if args.output:
                        fd.write(id)
                        fd.write("\n")
                    else:
                        print(id)
    if args.output:
        fd.close()