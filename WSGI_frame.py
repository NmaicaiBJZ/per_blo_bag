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
def index(static_path,ret):
    with open(static_path+'/home.html') as f:
        content = f.read()
    
    return content

# 匹配 /ras/fas/_markd_fasf.md 文件
@route("(.*?)_markd_(.*?.md)")
def markdown_handle(static_path,ret):
    # with open(static_path+ret.group(1)+ret.group(2)) as f:
    #     md_content = f.read()
    with open(static_path+'/read.html') as f:
        content = f.read()

    content = re.sub(r'\{%markdown_file%\}',ret.group(1)+ret.group(2),content)

    return content
    

def application(env,start_respense):
    # 返回响应的表头
    start_respense('200 OK' , [('Content-Type','text/html;charset=utf-8')])
    
    # 请求的文件名
    file_name = env['PATH_INFO']
    static_path = env['static_path']

    try:
        for url, func in URL_FUNC_DICT.items():   

            ret = re.match(url, file_name)
            if ret:             #判断ret是否为空，不为空调用func引用的函数
                return func(static_path,ret)
        else:
                with open(static_path+file_name) as f:
                    content = f.read()
                return content

    except OSError as ret:
        return f"请求的url{static_path+file_name}没有对应的文件。。<br>错误: {str(ret)}"
    except Exception as ret:
        return "产生异常：%s" %str(ret)