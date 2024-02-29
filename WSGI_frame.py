import re

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
    print(opt['login_true'])
    if opt['login_true']:
        with open(static_path+'/setting.html', encoding="utf-8") as f:
            content = f.read()
    else:
        with open(static_path+'/login.html', encoding="utf-8") as f:
            content = f.read()
    content = re.sub(r'\{%login_error%\}','',content)    

    return content

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
    except Exception as ret:
        return "产生异常：%s" %str(ret)