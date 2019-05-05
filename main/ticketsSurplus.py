import urllib.request
import json
import pandas as pd
from Constants.cons import *

# 余票查询
class ticketsSurplus:
    def __init__(self,fromStation,toStation,trainDate):
        self.fromStation = fromStation
        self.toStation = toStation
        self.trainDate = trainDate

    # 将站点字符串转化为字典
    @staticmethod
    def strToDict(stationName):
        codeDict = dict()
        stationList = stationName.split("@")
        for k in stationList:
            if len(k) > 0:
                thisCode = k.split("|")
                codeDict[thisCode[1]] = thisCode[2]
        return codeDict

    # 获取12306余票信息
    def ticketRearch(self):
        codeDict = ticketsSurplus.strToDict(stationName)
        comUrl = url.format(self.trainDate, codeDict[self.fromStation], codeDict[self.toStation])
        req = urllib.request.Request(comUrl)
        req.headers = header
        html = urllib.request.urlopen(req)
        dict = json.loads(html.read())
        return ticketsSurplus.dictToDataFrame(dict)

    # 将爬取的数据转化为DataFrame
    @staticmethod
    def dictToDataFrame(myDict):
        resultData = pd.DataFrame(columns=['车次', '商务座', '一等座', '二等座', '高级软卧', '软卧一等卧', '硬卧二等卧', '硬座', '无座'])
        myStrList = myDict['data']['result']
        for i in myStrList:
            myStr = str(i)
            myList = myStr.split("|")
            # ----------------------------------车次-------商务座------一等座----二等座----高级软卧--软卧一等座-硬卧二等卧--硬座----无座
            resultData.loc[len(resultData)] = [myList[3], myList[32], myList[31], myList[30], myList[21], myList[23],
                                               myList[28], myList[29], myList[26]]
        return resultData

if __name__ == '__main__':
    # 查询余票情况
    fromStation = "上海"
    toStation = '杭州'
    queryDate = "2019-05-21"
    tickets = ticketsSurplus(fromStation,toStation,queryDate)
    data = tickets.ticketRearch()
    print(data.loc[0])