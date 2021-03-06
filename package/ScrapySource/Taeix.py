# 每日收盤指數、漲跌、漲跌指數、漲跌百分比、成交量
import requests
from bs4 import BeautifulSoup
import pandas as pd
from package.Infrastructure import DateObj


class Taeix:
    def __init__(self, obj):
        self.dataDate = obj

    def GetTaeixList(self):
        url = "https://www.twse.com.tw/exchangeReport/MI_INDEX"
        data = {
            'response': 'json',
            'date': self.dataDate.strdate,
            'type': 'IND'
        }
        r = requests.post(url, data=data)
        data_json = r.json()
        taeix = data_json["data1"][1]
        # total = float((data_json["data3"][13][1]).replace(
        #     ',', '')) / 100000000  # 成交量(億元)
        # 漲跌指數
        taeix[2] = BeautifulSoup(taeix[2], 'html.parser').find('p').text
        taeix[2] = (taeix[2] == "-") and taeix[2] + taeix[3] or taeix[3]
        # 移除不必要的內容
        taeix.pop(3)
        # 漲跌百分比
        taeix[3] = formatFloat(taeix[3])

        # 成交量
        data["type"] = "MS2"
        r = requests.post(url, data=data)
        data_json = r.json()        
        total = float((data_json["data1"][0][1]).replace(
            ',', '')) / 100000000  # 成交量(億元)
        taeix.append(total)
        return taeix[1:]


def formatFloat(str):
    """    
    格式化float
    str:大盤指數漲跌百分比
    return float數字
    """
    try:
        p = float(str)
    except ValueError:
        p = 0

    return format(p / 100, '.4f')
