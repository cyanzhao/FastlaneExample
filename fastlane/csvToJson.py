#coding=utf-8
import csv
import types

def customSubList(index_s,index_e,rowlist):

    geziSublist = list()
    index = 0

    while index < len(rowlist):
        
        if index == 0:
            print ''
        else:
            perRowList = rowlist[index]
            subPerRowList = list()
            perIndex = 0
            for content in perRowList:
                if (perIndex >= index_s) & (perIndex <= index_e):
                    subPerRowList.append(content)
                    pass
                perIndex += 1
                pass
            
            if subPerRowList:
                geziSublist.append(subPerRowList)
                pass
            pass     
        
        index += 1

    return geziSublist

def jsonFromCSVList(rowlist):

    jsonString = ''
    mainKey = ''
    number = 0
    index = 0
    hasNoNull = False
    
    headRow = list()
    if len(rowlist):
        headRow = rowlist[0]
    else:
        pass

    if len(rowlist) == 1:
        #返回数组。。。。
        for content in headRow:
            jsonString += '\"' + content + '\"' + ','
            pass
    else:
        while (index < len(headRow)):
            key = headRow[index]
            number += 1
            if ((key != '') & (hasNoNull == True)) | (index == (len(headRow)-1)):
                value_count = number-1
                #将index_last引入进来
                if index == (len(headRow)-1):
                    if ((key != '') & (hasNoNull == False)):
                        mainKey = key
                        hasNoNull = True
                        value_count = number
                    elif ((key != '') & (hasNoNull == True)):
                        index -= 1
                    elif (key == ''):
                        value_count = number
                        pass
                else:
                    index -= 1

                #dict and array 的key 分别以{} 【】后缀
                if mainKey.endswith('{}'):
                    subRowList = customSubList(index-value_count+1,index,rowlist)
                    
                    # print '>>>>>>> {}' 
                    # print subRowList
                    mainKey = mainKey[:-2]
                    valueString = jsonFromCSVList(subRowList)
                    if valueString.endswith(','):
                        valueString = valueString[:-1]
                    jsonString = jsonString + '\"' + mainKey + '\"'  + ':' + '{' + valueString + '}' + "," 

                elif mainKey.endswith('[]'):
                    ##cyan目前暂时认定数组只包含一层，直接取value
                    # subRowList = customSubList(index-value_count+1,index,rowlist)
                    subRowList = customSubList(index-value_count+1,index,rowlist)
                    arrayList = list()
                    arrayList.append(subRowList[0])
                
                    # print '>>>>>>> []' 
                    # print arrayList
                    mainKey = mainKey[:-2]
                    valueString = jsonFromCSVList(arrayList)
                    if valueString.endswith(','):
                        valueString = valueString[:-1]
                    jsonString = jsonString + '\"' + mainKey + '\"'  + ':' + '[' + valueString + ']' + "," 

                else:
                    valueString = rowlist[1][index]
                    # print '>>>>>>> value:::' 
                    # print valueString
                    # jsonString = valueString
                    if mainKey.endswith('(bool)'):
                        mainKey = mainKey[:-6]
                        jsonString = jsonString + '\"' + mainKey + '\"'  + ':' + valueString +  ","
                    elif mainKey.endswith('(int)'):
                        mainKey = mainKey[:-5]
                        jsonString = jsonString + '\"' + mainKey + '\"'  + ':'  + valueString + ","
                    else:
                        jsonString = jsonString + '\"' + mainKey + '\"'  + ':' + '\"'  + valueString + '\"' + ","                
                        pass
                    pass
                hasNoNull = False
                number = 0

            elif (key != '') & (hasNoNull == False):
                mainKey = key
                hasNoNull = True
                          
                # print '1、-------' + mainKey

            else:            
                pass

            index += 1
            pass
        
    return jsonString

with open('./configSources/itunesCSV.csv', 'r') as f:
    f_csv = csv.reader(f)

 # row = row.split(',')
# 递归 直到 string or bool  int 
# 组织 header 的每一个key 
# key 对用的value 可能是： string / dict(key:value) / array
 
    oriRowlist = list()
    for row in f_csv:
        oriRowlist.append(row)
    jsonString = jsonFromCSVList(oriRowlist)
    if jsonString.endswith(','):
        jsonString = jsonString[:-1]
    jsonString = '[{' + jsonString + '}]'

    print '-------->最终： jsonString '
    print jsonString

    ##写入json 文件
    with open('./fastconfig.json','wt') as f:
        f.write(jsonString.decode('utf-8').encode('utf-8'))
    