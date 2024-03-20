import re
import json
import time
from os import remove

URL_FUNC_DICT = dict()


# 装饰器函数，便于扩展，为 URL_FUNC_DICT 添加函数，方便 application 调用
# 装饰器装饰后，内容为
# URL_FUNC_DICT={
#     "/index.html":index,
#     "/([^\.]+).md":markdown_handle
# }
def route(url):
    def set_func(func):
        #URL_FUNC_DICT["./index.py"] = index 用装饰器来装饰字典，不用在加上一个函数的同时给字典加入这个函数的调用
        URL_FUNC_DICT[url] = func
        def call_func(*args, **kwargs):
            return func(*args, **kwargs)
        return call_func
    return set_func
			
@route("/home.html")
def index(static_path,ret,opt):
    with open(static_path+'/home.html', encoding="utf-8") as f:
        content = f.read()
    return content

# 匹配 /ras/fas/_markd_fasf.md 文件
@route("(.*?)_markd_(.*?.md)")
def markdown_handle(static_path,ret,opt):
    # with open(static_path+ret.group(1)+ret.group(2)) as f:
    #     md_content = f.read()
    with open(static_path+'/read.html', encoding="utf-8") as f:
        content = f.read()

    content = re.sub(r'\{%markdown_file%\}',ret.group(1)+ret.group(2),content)

    return content
    
# 用于处理登录请求，如果登录成功返回cookie，使浏览器保存，如果登录失败则返回错误页面
@route("/login.php")
def page_login(static_path,ret,opt):
    if opt['login_true']:
        with open(static_path+'/setting.html', encoding="utf-8") as f:
            content = f.read()
        opt['start_respense']('200 OK',[('Content-Type','text/html;charset=utf-8'),('Set-Cookie','login_cookie')])
    else:
        with open(static_path+'/login.html', encoding="utf-8") as f:
            content = f.read()
        content = re.sub(r'\{%login_error%\}','登录失败，用户名或者密码错误',content) 

    return content

# 用于判断cookie是否通过，如果通过直接给予settin页面，如果不通过将返回登录页面，让用户验证通过
@route("/setting.html")
def login_judge(static_path,ret,opt):
    if opt['login_true']:
        with open(static_path+'/setting.html', encoding="utf-8") as f:
            content = f.read()
    else:
        with open(static_path+'/login.html', encoding="utf-8") as f:
            content = f.read()
    content = re.sub(r'\{%login_error%\}','',content)    

    return content

# 用于修改文件内容、标题、摘要与分类
# 用于添加文件内容、标题、摘要与分类
@route("/(add|revise)_article.php")
def opt_article(static_path,ret,opt):
    # 获取请求的指示
    option = ret.group(1)
    # ------WebKit 表示 http 表单 multipart/form-data 发送的数据会使用这个来分隔每个字符的数据
    target_sequence = b'------WebKit'
    # 用于 re 匹配到发送的 name 参数
    target_parameter = b'Content-Disposition:'
    # 这个代码的意义，当socket 的 recv 发现接收的数据后将有用来保存文件的代码，将首先发送头部，数据部分将全部分批发送给需要保存的文件中
    with open("./test","wb") as f:
        f.write(opt["file_option"])

    # 在文件流中读取数据，并将获得到的文件复制到新的文件夹中
    with open("./test","rb") as f:
        # 用于获取------WebKit下的所有数据
        data = b''
        # 判断是否到达------WebKit上面，预示着获取数据结束
        if_get_data = False
        # 判断是否处于需要保存的文件流中
        if_file_data = False
        # 创建一个字典用于保存到 resources 中的user.json文件中
        add_data = dict()

        # 用于遍历整个文件
        for line in f:
            if target_sequence in line:
                if if_get_data:
                    if if_file_data:
                        file_data = data
                        if_file_data = False
                    else:
                        parameter_data = data.decode("utf-8").strip('\r\n')
                    add_data[parameter_name] = parameter_data
                    if_get_data = False
                data = b''
            elif target_parameter in line:
                line_text = line.decode("utf-8")
                parameter_name = re.search(r'name=\"(.*?)\"',line_text).group(1)
                if parameter_name == option+"_article_content":
                    parameter_data = re.search(r'filename=\"(.*)"',line_text).group(1)
                    if_file_data = True
                if_get_data = True
            else:
                data += line

        # 用于测试json传送过来的数据是否正确
        print(add_data)

        # 将得到的文件保存在指定目录下
        with open(static_path+'/resources'+add_data[option+"_article_category"],"wb") as copy_f:
            copy_f.write(file_data)

        # 读取数据
        with open(static_path+"/resources/user.json","r",encoding="utf-8") as json_file:
            json_data = json.load(json_file)
            json_data.append({"filename":add_data[option+"_article_content"],"path":'./resources'+add_data[option+"_article_category"],"title":add_data[option+"_article_title"],"abstract":add_data[option+"_article_summary"],"time":time.strftime('%Y-%m-%d',time.localtime())})
        # 上锁
        opt['lock'].acquire()
        # 打开文件，当w打开的时候将会把文件删除
        try:
            with open(static_path+"/resources/user.json","w",encoding="utf-8") as json_file:
                json.dump(json_data, json_file, indent=4, ensure_ascii=False)
        except Exception as e:
            raise e
        finally:
            # 解锁
            opt['lock'].release()
        # print(json_data)
    return '修改成功'

# 用于添加文件内容、标题、摘要与分类
# @route("/add_article.php")
# def add_article(static_path,ret,opt):
#     pass

# 用于删除文件内容、标题、摘要与分类
@route("/remove_article.php")
def remove_article(static_path,ret,opt):
    print(opt["file_option"])
    # 读取数据
    with open(static_path+"/resources/user.json","r",encoding="utf-8") as json_file:
        json_data = json.load(json_file)
        # 删除对应路径的文件的json记录
        json_data = [i for i in json_data if  not opt["file_option"] in i["path"]+'/'+i["filename"]]
    # 上锁
    opt['lock'].acquire()
    # 打开文件，当w打开的时候将会把文件删除
    try:
        with open(static_path+"/resources/user.json","w",encoding="utf-8") as json_file:
            json.dump(json_data, json_file, indent=4, ensure_ascii=False)
    except Exception as e:
        raise e
    finally:
        # 解锁
        opt['lock'].release()

    remove(static_path+"/resources"+opt["file_option"])
    
    return ""

def application(env,start_respense):
    # 返回响应的表头
    start_respense('200 OK' , [('Content-Type','text/html;charset=utf-8')])
    
    # 请求的文件名
    file_name = env['PATH_INFO']
    static_path = env['static_path']
    # 设置字典
    opt = dict()
    # 字典设置操作是否成功登录
    opt["login_true"] = env["login_true"]
    # 字典设置响应的表头
    opt["start_respense"] = start_respense
    # 字典传入需要操作的值
    opt["file_option"] = env["file_option"]
    # 进程锁
    opt["lock"] = env['lock']

    try:
        for url, func in URL_FUNC_DICT.items():   

            ret = re.match(url, file_name)
            if ret:             #判断ret是否为空，不为空调用func引用的函数
                return func(static_path,ret,opt)
        else:
                with open(static_path+file_name, encoding="utf-8") as f:
                    content = f.read()
                return content

    except OSError as ret:
        return f"请求的url{static_path+file_name}没有对应的文件。。<br>错误: {str(ret)}"
    # except Exception as ret:
    #     return "产生异常：%s" %str(ret)