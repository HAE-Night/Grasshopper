"""有道翻译API的调用函数（封装为一个函数使用）"""
import json
import requests
import re


def translator(str):
    """
    input : str 需要翻译的字符串
    output：translation 翻译后的字符串
    """
    # API
    url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=null'
    # 传输的参数， i为要翻译的内容
    key = {
        'type': "AUTO",
        'i': str,
        "doctype": "json",
        "version": "2.1",
        "keyfrom": "fanyi.web",
        "ue": "UTF-8",
        "action": "FY_BY_CLICKBUTTON",
        "typoResult": "true"
    }
    # key 这个字典为发送给有道词典服务器的内容
    response = requests.post(url, data=key)
    # 判断服务器是否相应成功
    if response.status_code == 200:
        # 通过 json.loads 把返回的结果加载成 json 格式
        print(response.text)
        result = json.loads(response.text)
#         print ("输入的词为：%s" % result['translateResult'][0][0]['src'])
#         print ("翻译结果为：%s" % result['translateResult'][0][0]['tgt'])
        translation = result['translateResult'][0][0]['tgt']
        return translation
    else:
        print("有道词典调用失败")
        # 相应失败就返回空
        return None


def is_contains_chinese(strs):
    # for _char in strs:
    #     if '\u4e00' <= _char <= '\u9fa5':
    #         return True
    result = re.findall(r'[\u4e00-\u9fa5]', strs)
    return result


def List_cut(str_index):
    mindex = []  # 存放下标
    # 分词判断
    for ind in range(len(str_index)-1):
        if str_index[ind]+1 == str_index[ind+1]:
            if str_index[ind] not in mindex:
                mindex.append(str_index[ind])
            if str_index[ind+1] not in mindex:
                mindex.append(str_index[ind+1])
        else:
            mindex.append("-")
    return mindex


def Replace(CN, CNList, EGList):
    if CN in CNList:
        return EGList[CNList.index(CN)]
    else:
        return "不存在"


if __name__ == '__main__':
    strs = '喜定羊awdas 灰太狼ewgve 0225'
    NList = ["喜定羊", "灰太狼"]
    MList = ["XYY", "HTL"]

    CN_name = is_contains_chinese(strs)
    str_index = [strs.index(CN_name[i]) for i in range(len(CN_name))]

    Index_List = List_cut(str_index)
    CN_List = []
    # 字符串内文字拼接
    for il in Index_List:
        CN_List.append(strs[il]) if type(il) == int else CN_List.append(il)
    CN = "".join(CN_List).split("-")
    for CN_Name in CN:
        EG_Name = Replace(CN_Name, NList, MList)
        strs = strs.replace(CN_Name, EG_Name+" ")
    print(strs)