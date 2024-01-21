from collections import defaultdict
import re
import os
import json

def makeKeyAndValue_and_check(array:list):
    """
    将list整合成key [english_value,japanese_value]一一对应的dictionary.并且进行百分号核对
    参数: 只包含"key"="value"的list.

    逻辑说明: 使用正则表达式将list整合成
        dictionary{[key1,[% count, %@ count, %l count]],
                    [key2,[% count, %@ count, %l count]],...}.
                    [%的数量,%@的数量,%l的数量] 
    """
    check_dictionary = {}
    wrong_match = []
    wrong_check = []
    for i in array:
        pattern = r'(^|\s)\"(.+)\"\s=\s\"(.+)\";($|\/|\n|\s)'
        match = re.match(pattern, i)
        if match:
            key = match.group(2)
            value = match.group(3)
            #[%,%@,%l,\“] 暂时不做\“检查
            # print(key +'and'+value)
            #setdefault方法 当key存在的时候不做改变，当key不存在的时候初始值设为 key,[-1,-1,-1]
            check_dictionary.setdefault(key,[-1,-1,-1])
            if check_dictionary[key][0] == -1 or value.count('%') == check_dictionary[key][0]:
                check_dictionary[key][0] = value.count('%')
            else:
                check_dictionary[key][0] = value.count('%')
                wrong_check.append(i)
                #有任何一个检测出错 剩下的检查就可以不做了 直接continue检查下一句
                continue
            if check_dictionary[key][1] == -1 or value.count('%@') == check_dictionary[key][1]:
                check_dictionary[key][1] = value.count('%@')
            else:
                check_dictionary[key][0] = value.count('%@')
                wrong_check.append(i)
                continue
            if check_dictionary[key][2] == -1 or value.count('%l') == check_dictionary[key][2]:
                check_dictionary[key][2] = value.count('%l')
            else:
                check_dictionary[key][0] = value.count('%l')
                wrong_check.append(i)
                continue
            # if result[key][3] == -1 or value.count('\\"') == result[key][3]:
            #     result[key][3] = value.count('\\"')
            # else:
            #     wrong_check.append(i)
            #     continue
        else:
            wrong_match.append(i)
            # print("These string :" + i +" is not be patterned")
    """
    检测结果需要替换成自己机器的path

    no_match(wrong_match):表示不能匹配到上面的正则表达式
    no_check(wrong_check):表示出现错误的字串
        错误字串的key将会被输出两遍
        因为以上逻辑检测到的%、%@、%l不符合的情况 将会被输出两次
    """
    no_match = '/Users/haru.feng/Downloads/wrong_match.txt'
    no_check = '/Users/haru.feng/Downloads/wrong_check.txt'
    with open (no_match,'w') as file:
        file.write('\n'.join(wrong_match))
    with open (no_check,'w') as file:
        file.write('\n'.join(wrong_check))

#核对检测字典
    # with open('/Users/haru.feng/Downloads/dictionary.txt', "w") as file:
    #     if not os.path.exists('/Users/haru.feng/Downloads/result.txt'):
    #         print('Your local Language result file not exist at path: /Users/haru.feng/Downloads/result.txt')
    #         return
    #     jsobj = json.dumps(result)
    #     file.write(jsobj)

    # return result

# def testcheck():
#     list = '"unassigned participant" = "nicht-zugewiesener Teilnehmer";'
#     pattern = r'\"(.+)\"\s=\s\"(.+)\";(\s|\/|\n|$)'
#     match = re.match(pattern, list)
#     if match :
#         key = match.group(1)
#         value = match.group(2)
#         print(key," % value number is :",value.count('%'))
#         print(key," %@ value number is :",value.count('%@'))
#         print(key," %l value number is :",value.count('%l'))
#         print(key," \" value number is :",value.count('\"'))
#     else:
#         print("wrong")


def filter_string_with_path(path:str)->list:
    """
    从path文件读取出来的str->只包含"key"="value"的list 
    注 过滤掉了注释和空白的行

    参数: 
        path(str) 所有语言lproj文件的上一级目录.
    返回值: 
        只包含"key"="value"的list.
    """
    #全部16种语言的文件夹简写
    localization_file_name = ['de','en','es','fr','id','it','ja','ko-KR','nl','pl','pt-PT','ru','tr','vi','zh-Hans','zh-Hant']
    content = []

    for lan_file_name in localization_file_name:
        filepath = path + '/' + lan_file_name + '.lproj/Localizable.strings'
        temp = filter_one_file(filepath)
        content = content + temp
        
    return content

def filter_one_file(filepath:str) -> list:
    if not os.path.exists(filepath):
        print('Your local Language file not exist at path: ' + filepath +' ,please do not use the contents do any analysis.')
        return
    content = []
    lines = []
    # /* 开始的标记
    flag = False
    with open(filepath, 'r') as file:
        lines =  file.readlines()
        file.close()
    for line in lines:
        if flag == True:
            if line.endswith('*/'):
                flag = False
            continue
        line = line.strip()
        if line.startswith(('//'))  or (line in ['\n','\r\n']):
            continue
        if line.startswith('/*') :
            if line.endswith('*/'):
                continue
            else:
                flag = True
                continue
        # content.append(line)
        content.append(line)
    return content
