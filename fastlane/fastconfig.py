import os
import json
from pprint import pprint
import types

print '------------------------->' + os.name

# value type: string bool number
def organizeBaseDic(baseDic,dotEnabled):
    deliverString = ''
    lanList = list()
    if baseDic.has_key('supportedLanguages'):
        lanList = baseDic['supportedLanguages']

    for key in baseDic.keys():
        value = baseDic[key]
        if type(value) is types.UnicodeType:
            deliverString += key + ( ':' if dotEnabled else '') + ' ' + '\"' + value + '\"' + ( ',' if dotEnabled else '') + '\n'
        
        if type(value) is types.BooleanType:
            boolString = 'false'
            if value == True:
                boolString = 'true'
            deliverString += key + ( ':' if dotEnabled else '') + ' '  + boolString  + ( ',' if dotEnabled else '') + '\n'
    
        if type(value) is types.IntType:
            deliverString += key + ( ':' if dotEnabled else '') + ' ' + str(value) + ( ',' if dotEnabled else '') + '\n'

        if type(value) is types.DictionaryType:
            isLankey = False
            for lanSupport in lanList:
                if key == lanSupport:
                    isLankey = True
                    break
            if isLankey ^ 1:
                deliverString += key + '({' + '\n'
                deliverString += organizeBaseDic(value,True)
                deliverString += '})' + '\n' 
                

        if type(value) is types.ListType:
            if key == 'supportedLanguages':
                lanReList = list()      
                for basekey in baseDic.keys():
                    for lan in lanList:
                        if basekey == lan:
                            baselanDic = baseDic[basekey]   
                            if type(baseDic) is types.DictionaryType:
                                for lanItemkey in baselanDic.keys():
                                    exsitLanDic = None
                                    for lanReItemDic in lanReList:
                                        if lanReItemDic.has_key(lanItemkey):
                                            exsitLanDic = lanReItemDic[lanItemkey]
                                    if exsitLanDic:
                                        exsitLanDic[lan] = baselanDic[lanItemkey]
                                    else:
                                        newLanDic = {lan:baselanDic[lanItemkey]}
                                        newItemDic = {lanItemkey:newLanDic}
                                        lanReList.append(newItemDic)
                #organize lanReList to deiverstring
                for lanItemDic in lanReList:
                    lanKey = lanItemDic.keys()[0]
                    lanDic = lanItemDic[lanKey]
                    print lanKey + '-----------'
                    deliverString += lanKey + '({' + '\n'
                    for lanInfoKey in lanDic.keys():
                        lanInfoValue = lanDic[lanInfoKey]
                        deliverString += '\'' +lanInfoKey + '\'' + ' => ' + '\"' + lanInfoValue + '\"' + ',\n'
                    
                    deliverString += '})' + '\n'
            else:
                pass
    
    return deliverString  



# //parse json --> model --> deliverFile
class JSONObject:
    def __init__(self, d):
        self.__dict__ = d

with open('./fastconfig.json', 'r') as f:

    #json to model
    # data = json.load(f,object_hook=JSONObject)
    data = json.load(f)
    configDic = data[0]
    deliverString = 'Encoding.default_external = Encoding::UTF_8\nEncoding.default_internal = Encoding::UTF_8\n\n' + organizeBaseDic(configDic,False)

#write to file 
with open('Deliverfile','wt') as f:
    f.write(deliverString.encode('utf-8'))


