import json, datetime, os
from nonebot import require

require("nonebot_plugin_localstore")

import nonebot_plugin_localstore as store

async def writeIn(text: str, userID: str):
    #main
    date = str(datetime.datetime.now())[0:19]
    data = text.split()
    dataDic = {}
    innerDataDic = {'location': data[0], 'person': data[1], 'price': data[2], 'by': userID}
    dataDic[date] = innerDataDic
    data_dir = store.get_data_dir("groupAccountant")
    jsonFile = store.get_data_file('groupAccountant', 'accountant_book.json')
    print(jsonFile)
    if os.path.getsize(jsonFile) == 0:
        dataJson = json.dumps(dataDic)
        jsonFile.write_text(dataJson)
    else:
        jsonFileData = jsonFile.read_text()
        dataJson = json.loads(jsonFileData)
        print(dataJson)
        dataJson.update(dataDic)
        dataJson = json.dumps(dataJson)
        jsonFile.write_text(dataJson)
        #print(4)
    return(data_dir)

async def readBook(clear: bool):
    jsonFile = store.get_data_file('groupAccountant', 'accountant_book.json')
    if os.path.getsize(jsonFile) == 0:
        resp = '当前无账目信息'
        return resp
    jsonFileData = jsonFile.read_text()
    dataDic = json.loads(jsonFileData)
    resp = ''
    for key in dataDic:
        resp += str(key + '在' + dataDic[key]['location'] + '，' + dataDic[key]['person'] + '人，消费了' + dataDic[key]['price'] + '元，由'+dataDic[key]['by']+'记录\n')
    if clear == True:
        jsonFile.write_text('')
        resp += '账目已最终清算，账本清除'
    return resp
        