
import math

# 十度方区换算
'''
后两位表示经度，东西经各18区，编号为 00~17；

前两位分得不是很清楚，大概规则如下：

第1位有四个数字，分别是 1,3,5,7
1 的范围是 0N0E（左下角） 到 90N180E（右上角），
3 的范围是 0S0E（左上角） 到 90S180E（右下角），
5 的范围是 0S0W（右上角） 到 90S180W（左下角），
7 的范围是 0N0W（右下角） 到 90N180W（右下角），

第2位数字则是按照纬度从赤道向两极，南北各划分9个区域，数字范围是 0~8

'''
def georect_convert(rect_num):
    rect_num = int(rect_num)
    rdigits = rect_num % 100
    lont = rdigits * 10

    ldigits = (rect_num - rdigits) / 100
    lat = (ldigits % 10) * 10

    divide_num = int(math.floor(ldigits / 10))

    area = {
        'tl': {
            'lat': -1,
            'lon': -1,
        },
        'br': {
            'lat': -1,
            'lon': -1,
        }
    }
    if divide_num == 1:
        area['tl']['lon'] = lont
        area['tl']['lat'] = lat + 10
        area['br']['lon'] = lont + 10
        area['br']['lat'] = lat
    elif divide_num == 3:
        area['tl']['lon'] = lont
        area['tl']['lat'] = -lat
        area['br']['lon'] = lont + 10
        area['br']['lat'] = -lat - 10
    elif divide_num == 5:
        area['tl']['lon'] = -lont - 10
        area['tl']['lat'] = -lat
        area['br']['lon'] = -lont
        area['br']['lat'] = -lat - 10
    elif divide_num == 7:
        area['tl']['lon'] = -lont - 10
        area['tl']['lat'] = lat + 10
        area['br']['lon'] = -lont
        area['br']['lat'] = lat

    return area

print(georect_convert(3311))
