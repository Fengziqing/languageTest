import git
from unidiff import PatchSet
from io import StringIO
"""
        get_diff.py 
        这个文件主要是对PatchSet的封装
        开发者能够使用这些方法更加简单的取到自己想要的信息
"""

class ChangedLine:
    """ 
        用来存放一行改动有关的信息

        file_path 这一行改动的所存在的文件地址 
        line_number 这一行改动的行数 
        content 这一行改动的内容
        author 这一行对应的作者
    """
    file_path: str
    line_number: int
    content: str
    author: str
    date_and_time: str

def get_uncommited_diff_text(rep:str):
    """ 
    取到本地未提交的全部的diff内容.
    【【【【一般作为本文件其他操作的第一步】】】】

    参数:
        rep: string 某个带有git文件的path
        例如 '/Users/haru.feng/Documents/SourceCode/ep-new-release/mac-client'

    返回值: 
        diff_text

    错误情况 
        传入的path没有对应的git文件
    """
    repository = git.Repo(rep)
    #repository.head.commit.tree为本地没有提交过的sha 也就是head值 取到diff.
    commit_sha = repository.head.commit.tree
    diff_text = repository.git.diff(commit_sha)

    return diff_text

def get_added_localizable_string(diff_text) -> list:
    """ 
    是用来取到仅仅只是localizable.string文件内的、添加行的改动.

    参数:
        diff_text:必须是由git.diff取到的diff text 
        例如由get_uncommited_diff_text取到的diff_text

    返回值:
        list 仅仅是localizable.string结尾的文件里添加行的改动
    """
    patches = PatchSet(StringIO(diff_text))
    add_contents = []
    for p in patches:
        if p.added > 0:
            for h in p:
                for i, line in enumerate(h):
                    #提取出来标识为is_added 和 path由Localizable.strings结尾的line,加入diff_contents里.
                    if line.is_added and p.path.endswith('Localizable.strings'):
                        add_contents.append(line.value)
    return add_contents

def get_all_added_file(diff_text) -> list:
    """
    取到所有添加的文件的路径
    注 只是文件本身的增加 并不是关于文件内容的增加

    参数:
        diff_text:必须是由git.diff取到的diff text
        例如由get_uncommited_diff_text取到的diff_text

    返回值:
        含有所有添加文件路径的list
    """
    patches = PatchSet(StringIO(diff_text))
    changed_files_path = []
    for p in patches:
        if p.is_added_file:
            changed_files_path.append(p.path)
    return changed_files_path

def get_all_deleted_file(diff_text) -> list:
    """
    取到所有被删除的文件路径
    注 只是文件本身的删除 并不是关于文件内容的删除

    参数:
        diff_text:必须是由git.diff取到的diff text
        例如由get_uncommited_diff_text取到的diff_text

    返回值:
        含有所有被删除文件路径的list
    """
    patches = PatchSet(StringIO(diff_text))
    changed_files_path = []
    for p in patches:
        if p.is_removed_file:
            changed_files_path.append(p.path)
    return changed_files_path

def get_all_modified_file(diff_text) -> list:
    """
    取到所有被修改的文件路径
    注 只是文件本身的修改 并不是关于文件内容的修改

    参数:
        diff_text:必须是由git.diff取到的diff text
        例如由get_uncommited_diff_text取到的diff_text

    返回值:
        含有所有被修改文件路径的list
    """
    patches = PatchSet(StringIO(diff_text))
    changed_files_path = []
    for p in patches:
        if p.is_modified_file:
            changed_files_path.append(p.path)
    return changed_files_path

def get_added(diff_text) -> [ChangedLine]:
    """
    返回所有的添加行

    参数:
        diff_text:必须是由git.diff取到的diff text
        例如由get_uncommited_diff_text取到的diff_text

    返回值:
        由ChangedLine组成的数组
    """
    patches = PatchSet(StringIO(diff_text))
    added_lines = []
    for p in patches:
        if p.added > 0:
            for h in p:
                for i, line in enumerate(h):
                    if line.is_added:
                        temp = ChangedLine()
                        temp.content = line.value
                        temp.file_path = p.path
                        temp.line_number = line.target_line_no
                        added_lines.append(temp)
    return added_lines

def get_deleted(diff_text) -> [ChangedLine]:
    """返回所有删除的行
    参数:
        diff_text:必须是由git.diff取到的diff text
        例如由get_uncommited_diff_text取到的diff_text
    返回值:
        由ChangedLine组成的数组
        注 每个删除行的line_number将会是None
    """
    patches = PatchSet(StringIO(diff_text))
    deleted_lines = []
    for p in patches:
        if p.removed > 0:
            for h in p:
                for i, line in enumerate(h):
                    if line.is_removed:
                        temp = ChangedLine()
                        temp.content = line.value
                        temp.file_path = p.path
                        temp.line_number = line.target_line_no
                        deleted_lines.append(temp)
    return deleted_lines

def get_content_changed_file(diff_text) -> list:
    """
    得到某个diff 所有的 存在改动的 文件列表
        diff_file_list 与 get_deleted()、get_added()返回的ChangeLine里的path有什么区别呢?
            1 diff_file_list 不会有重复的path
            2 get_deleted()、get_added()返回的ChangeLine里的path需要与add_lines一一对应, 所以有重复的值
        参数:
            diff_text:必须是由git.diff取到的diff text
            例如由get_uncommited_diff_text取到的diff_text
        返回值:
            只包含更改后的文件列表
    """
    patches = PatchSet(StringIO(diff_text))
    diff_file_list = []
    for p in patches:
        diff_file_list.append(p.path)
    return diff_file_list

def get_content_changed_line_number(diff_text) -> list:
    """
    得到某个diff 所有的 改动行数
        参数:
            diff_text:必须是由git.diff取到的diff text
            例如由get_uncommited_diff_text取到的diff_text
        返回值:
            只包含更改后所有 行数list[int] 不做文件的区分
    """
    patches = PatchSet(StringIO(diff_text))
    line_numbers = []
    for p in patches:
        for h in p:
            for i, line in enumerate(h):
                if line.is_removed or line.is_added:
                    line_numbers.append(line.target_line_no)
    return line_numbers

def get_line_merge_time(path:str, line_start:int, line_end:int):
    """
    得到某一个行或者某一个范围内行数的 提交时间 : *只得到 提交时间 不包含其他信息* 
    等于是对 get_line_author_data 返回值的解析
        参数:
            path: 
                location目录下你需要查询的文件地址
                例如'/Users/haru.feng/Documents/SourceCode/ep-new-release/mac-client/VideoUI/VideoUI/Toolbar/ZPConfToolbarController.mm'
            
            L 需要查找的行数 L= '<line_start>,<line_end>' line_start、line_end 一致表示只搜索这一行
            ·例如 163,163(只查询163行)
            ·163,+5(查询163开始的5行)
            ·163,167(查询163到167行) 
            参数参考自 https://git-scm.com/docs/git-blame/en
            
            line_start:string
                L 的第一个行参数line_start
            line_end:string
                L 的第二个行参数line_end
        返回值:
            如果输入的行数是一行 那么会返回time的str
            如果输入的行数是一个范围 那么会返回由time的str组成的list
    """
    data = get_line_author_data(path, line_start, line_end)
    mark = line_start
    if line_start != line_end:
        # 有多行的查询 就返回list[str]
        date_time = []
        for item in data.splitlines():
            start_mark = item.index(str(mark) + ')') - 26
            # magic number: 27这个数字是根据格式硬数出来的 ‘2018-12-27 15:12:46 +0800 ’
            end_mark = item.index(str(mark) + ')') - 7
            date_time_str = item[start_mark:end_mark]
            #除去右边的空格
            date_time.append(date_time_str)
            mark = mark + 1
    else:
        start_mark = data.index(str(mark) + ')') - 26
        # magic number: 27这个数字是根据格式硬数出来的 ‘2018-12-27 15:12:46 +0800 ’
        end_mark = data.index(str(mark) + ')') - 7
        date_time = data[start_mark:end_mark]
    return date_time

    #以下是对 get_line_author_data 返回值的解析
#！！！！！！！！提交时间？？！！！！！！！！！检查出没有送翻的字串会有一定参考价值

def get_line_author(path:str, line_start:int, line_end:int):
    """
    得到某一个行或者某一个范围内行数的作者: *只得到作者不包含其他信息* 
    等于是对 get_line_author_data 返回值的解析
        参数:
            path: 
                location目录下你需要查询的文件地址
                例如'/Users/haru.feng/Documents/SourceCode/ep-new-release/mac-client/VideoUI/VideoUI/Toolbar/ZPConfToolbarController.mm'
            
            L 需要查找的行数 L= '<line_start>,<line_end>' line_start、line_end 一致表示只搜索这一行
            ·例如 163,163(只查询163行)
            ·163,+5(查询163开始的5行)
            ·163,167(查询163到167行) 
            参数参考自 https://git-scm.com/docs/git-blame/en
            
            line_start:string
                L 的第一个行参数line_start
            line_end:string
                L 的第二个行参数line_end
        返回值:
            如果输入的行数是一行 那么会返回author的str
            如果输入的行数是一个范围 那么会返回由author的str组成的list
    """
    author_data = get_line_author_data(path, line_start, line_end)
    #以下是对 get_line_author_data 返回值的解析
    mark = line_start
    if line_start != line_end:
        # 有多行的查询 就返回list[str]
        author = []
        for item in author_data.splitlines():
            start_mark = item.index('(') + 1
            # magic number: 27这个数字是根据格式硬数出来的 ‘2018-12-27 15:12:46 +0800 ’是这一段的字数+1
            end_mark = item.index(str(mark) + ')') - 27
            author_str = item[start_mark:end_mark]
            #除去右边的空格
            author.append(author_str.rstrip())
            mark = mark + 1
    else:
        # 只有一行的查询 就返回str
        start_mark = author_data.index('(') + 1
        end_mark = author_data.index(str(mark) + ')') - 27
        author = author_data[start_mark:end_mark]
        #除去右边的空格
        author = author.rstrip()
    return author

def get_line_author_data(path:str, line_start:int, line_end:int,
                            show_file:bool=True, show_line_number:bool=True) -> str:
    """ 
    得到某个文件中的某一行的(或某个范围的) *author相关信息* 
        需要指定文件位置和行数信息.
        参数:
            location(deprecated/已弃用):
                需要检查的path
                注 应该是包含.git文件的目录
                例如'/Users/haru.feng/Documents/SourceCode/ep-new-release/mac-client'
            path: 
                location目录下你需要查询的文件地址
                例如'/Users/haru.feng/Documents/SourceCode/ep-new-release/mac-client/VideoUI/VideoUI/Toolbar/ZPConfToolbarController.mm'
            
            L 需要查找的行数 L= '<line_start>,<line_end>' line_start、line_end 一致表示只搜索这一行
            ·例如 163,163(只查询163行)
            ·163,+5(查询163开始的5行)
            ·163,167(查询163到167行) 
            参数参考自 https://git-scm.com/docs/git-blame/en
            
            line_start:string
                L 的第一个行参数line_start
            line_end:string
                L 的第二个行参数line_end

            show_file=true显示文件名 
            show_line_number:默认值True
                是否显示行数 
        color_by_age对应color-by-age:给注释附着颜色 

        返回值:
            只包含更改后所有行数 不做文件的区分
            *author相关信息* :
            类似于: [34m3247ec91e46 ChatUI/Diagnostic/ZMDiagnosticBar.m 18 (Huxley 2018-12-27 15:12:46 +0800 18) [m    ZMReleaseToNil(_warningForegroundColor);
    """
    #默认只查询 mac-client 底下的信息所以在这里自动取到 mac-client 的 git repo
    mark_string = 'mac-client/'
    mark_string_index = path.index('mac-client/')
    mark_string_len = len(mark_string)
    location = path[:mark_string_index] + 'mac-client'
    temp_mark = mark_string_index + mark_string_len 
    path = path[temp_mark:]
    repo = git.Repo(location)

    """
        path=mac-client下你需要查询的文件目录

        L 需要查找的行数 L= '<line_start>,<line_end>'
        start、end一致表示只搜索这一行
        例如 163,163(只查询163行) or 163,+5(查询163开始的5行) or 163,167(查询163到167行) 
        参数信息参考网站 https://git-scm.com/docs/git-blame/en

        f=true显示文件名 
        n=true显示行数 
        color_by_age对应color-by-age:给注释附着颜色 

    """
    result = repo.git.blame(path, L=f'{line_start},{line_end}', f=show_file, 
                            n=show_line_number, color_by_age=True)
    return result

def get_commit_author(location:str, commit_sha:str) -> str:
    """ 
    得到某次commit的作者
    
    参数:
        location:
            需要检查的目录 
            例如'/Users/haru.feng/Documents/SourceCode/ep-new-release/mac-client'
        commit_sha:
            commit的sha号
    
    返回值:
        format 为 Author: 名字 <时间>的字串
    """
    repo = git.Repo(location)
    author = repo.git.show("-s", "--format=Author: %an <%ae>", commit_sha)
    return author

# if __name__ == '__main__': 
    # 使用例
    # diff_text = get_uncommited_diff_text('/Users/haru.feng/Documents/SourceCode/ep-new-release/mac-client')
    # author = get_line_author('/Users/haru.feng/Documents/SourceCode/ep-new-release/mac-client/VideoUI/VideoUI/Toolbar/ZPConfToolbarController.mm',1243,1245)
    # print(author)
    # result = get_added(diff_text)
    # result = get_content_changed_line_number(diff_text)
    # print(result)