#扫描所有xcodeproject文件 找出.localiation后缀的key 查找key是否存在
from pbxproj import XcodeProject
import classify_and_check
import os
import re
import get_diff
from os import path
import os
import fnmatch

#check_objc_files_string_exist:判断输入的文件里 .localizatedstring 前的key是否存在
#!!!!!!!!注意 clips transcode 需要分开检测，所以使用的set应该是自己独有的 不应该共用set!!!!!!!
def check_objc_files_string_exist(files_path: list, all_eng_key_set: set) -> [get_diff.ChangedLine]:
    result = []
    #遍历所有的 m_mm_h_files_path 文件
    for path in files_path:
        #找到文件内部所有的以 .localizableString结尾的key
        key_array = get_file_key_array(path)
        #进行核对 找出未提交的字串所在的代码位置 file path
        for key in key_array:
            if key not in all_eng_key_set:
                temp_changed_line = get_diff.ChangedLine()
                temp_changed_line.file_path = path
                temp_changed_line.content = key
                result.append(temp_changed_line)
                #只打印key和所存在的文件名（path.rsplit('/',1)[-1]）：开发需要自己找到对应文件里的对应key 并且自己核对。重点在于找到某一行的author并且做出总结以减少工作量。
                # print("KEY: \n"+ key + "\nLOCATION: \n" + path.rsplit('/',1)[-1] + "\ndo not have english string. \n")
    #填入对应的line number
    find_line_number(result)
    #填入对应的author
    find_author(result)
    #填入对应的date and time
    find_date_and_time(result)
    return result

def find_author(items:[get_diff.ChangedLine()]) -> [get_diff.ChangedLine()]:
    for i in items:
        if not os.path.exists(i.file_path):
            print('Your get_diff.ChangedLine file_path is not correct: ' + i.file_path)
            return items
        i.author = get_diff.get_line_author(i.file_path,i.line_number,i.line_number)
    return items

def find_date_and_time(items:[get_diff.ChangedLine()]) -> [get_diff.ChangedLine()]:
    for i in items:
        if not os.path.exists(i.file_path):
            print('Your get_diff.ChangedLine file_path is not correct: ' + i.file_path)
            return items
        i.date_and_time = get_diff.get_line_merge_time(i.file_path,i.line_number,i.line_number)
    return items

def find_line_number(items:[get_diff.ChangedLine()]) -> [get_diff.ChangedLine()]:
    for i in items:
        if not os.path.exists(i.file_path):
            print('Your get_diff.ChangedLine file_path is not correct: ' + i.file_path)
            return items
        
        lines = []
        with open(i.file_path, 'r') as file:
            lines =  file.readlines()
            file.close()
        #逐行比对
        line_mark:int = 0
        for line in lines:
            line_mark = line_mark + 1
            if i.content in line:
                i.line_number = line_mark
                break

    return items

#get_file_key_array:取一个path（.m .mm .h）文件里所有的 .localizatedstring前的key
def get_file_key_array(file_path:str)->list:
    if not os.path.exists(file_path):
        print('Your local .m/.h/.mm file not exist at path: ' + file_path)
        return []
        
    key_value_list = []
    pattern = r'@\"([\w\s\d]+)\".localizedString'
    #过滤掉 注释的行 和 空行
    lines = classify_and_check.filter_one_file(file_path)
    for line in lines:
        #如果有一行有好几个key 需要用findall全部取出
        match = re.findall(pattern,line)
        if match :
            for item in match:
                key_value_list.append(item)

    return key_value_list

#find_m_mm_h_files:找到所有以.m .mm .h 结尾的文件 返回文件路径list
def find_m_mm_h_files(root_dir: str,independent_files:list) -> list:
    if not os.path.exists(root_dir):
        print('Your xcode project file not exist at path: ' + root_dir)
        return []
    m_mm_h_files_path = []
    no_reference_file = ['ZMChatMsgItemView.mm','ZPMenuWindowController.mm','ZMConfTopbarView.mm']
    for root, _, files in os.walk(root_dir):
        flag:bool = True
        for inde_file_name in independent_files:
            if inde_file_name in root:
                flag = False
        if flag is False:
            continue
        for file in files:
            if fnmatch.fnmatch(file, '*.mm'):
                if file in no_reference_file:
                    continue
                m_mm_h_files_path.append(os.path.join(root, file))
            elif fnmatch.fnmatch(file, '*.m'):
                m_mm_h_files_path.append(os.path.join(root, file))
            elif fnmatch.fnmatch(file, '*.h'):
                m_mm_h_files_path.append(os.path.join(root, file))
    return m_mm_h_files_path

#get_all_key:拿到文件里的所有key value -> set
#哈希set 查找速度更快
def get_all_key(file_path:str) -> set:
    #path 判断
    if not os.path.exists(file_path):
        print('Your file not exist at path: ' + file_path)
        return []
    
    #过滤掉英文文件里的空格和注释
    file_string = classify_and_check.filter_one_file(file_path)
    all_eng_keys = set()
    for line in file_string:
        #正则表达式
        pattern = r'(^|\s)\"(.+)\"\s=\s\"(.+)\";($|\/|\n|\s)'
        match = re.match(pattern, line)
        if match:
            #group2是key所在的位置
            all_eng_keys.add(match.group(2))
            # print(match.group(2))
    return all_eng_keys

def write_to_file(path:str,array:list):
    if not os.path.exists(path):
        print('Your translated file not exist at path: ' + path)
        return
    with open(path, 'a') as file:
        for i in array:
            file.write("file path: " + i.file_path)
            file.write('\n')
            file.write("string: " + i.content)
            file.write('\n')
            file.write("line number: " + str(i.line_number))
            file.write('\n')
            file.write("author: " + i.author)
            file.write('\n')
            file.write("merge time: " + i.date_and_time)
            file.write('\n\n')
        # for i in array:
        #     file.write(i.content)
        #     file.write(i.file_path)
        # file.write('\n'.join(array))
        # file.write(array)

if __name__ == '__main__':
    #!!!!!!!!!!!!!!!!!文件路径需要统一包装一下 不要手动输入了
    #需要 除去 这种自己带语言文件的，这种的需要分开检查，字串不通用 所以set不通用。
    independet_project_array = ['ZoomClips','Transcode','ZoomAutoUpdater']
    #英文string文件路径
    english_string_path = '/Users/haru.feng/Documents/SourceCode/ep-new-release/mac-client/Zoom/Zoom/Zoom/en.lproj/Localizable.strings'
    #拿到所有的英语的key组成的set
    all_eng_key_set = get_all_key(english_string_path)
    
    #需要扫描的文件父目录
    root_dir = ('/Users/haru.feng/Documents/SourceCode/ep-new-release/mac-client')
    #得到所有以 .m .h .mm结尾的文件路径
    m_mm_h_files_path = find_m_mm_h_files(root_dir,independet_project_array)
    result = check_objc_files_string_exist(m_mm_h_files_path,all_eng_key_set)
    write_to_file('/Users/haru.feng/Downloads/result.txt',result)
    # independet_project_array = ['ZoomClips','Transcode']
    # root_dir = ('/Users/haru.feng/Documents/SourceCode/release-client-5.15.1/mac-client')
    # m_mm_h_files_path = find_m_mm_h_files(root_dir,independet_project_array)
    # print(m_mm_h_files_path)

    # path = '/Users/haru.feng/Documents/SourceCode/release-client-5.15.1/mac-client/VideoUI/VideoUI/Chat/NewChatMessage/ZMMeetingMessageMenuImpl.mm'
    # key = get_file_key_array(path)
    # print(key)


    
    #git blame ZPChatInMeetingWindowCtrl.mm -L <begin,after>



    

    