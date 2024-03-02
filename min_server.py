import re
import socket
#import WSGI_frame
# import sys
import multiprocessing
from time import sleep

#注意：使用此程序需要使用当前目录下的html目录里面的html文件
#html文件使用带有超链接的最好，最好可以有图片
class WSGI_mini_web(object):
    def __init__(self,port,app,static_path,useranme,userpassword):
        self.tcp_server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.tcp_server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.tcp_server_socket.bind(('',port))
        self.tcp_server_socket.listen(128)
        self.application = app
        self.static_path = static_path
        self.useranme = useranme
        self.userpassword = userpassword
    def server_client(self,new_socket):
        """为客户端返回数据"""
        #接收发送过来的数据
        repuest = new_socket.recv(1024).decode("utf-8")
        repuest_lines = repuest.splitlines()  # 将数据转为列表
        print("")
        print(">" * 10)
        
        #将数据答应到控制台
        print(repuest_lines)

        #为客户端返回数据
        file_name = ""
        """数据接收到  get /.... 1.1 ...
                正则表达式匹配该文件的地址"""
        ret = re.match(r"([^/]+)([^ ]*)",repuest_lines[0])

        # 判断是否能直接通过
        login_true = False
        # 判断cookie是否存在
        cookie_v = ''
        # 关于form提交需要添加或者修改的内容
        file_option = b''

        if ret:
            file_name = ret.group(2)
            if file_name == "/":
                file_name = "/home.html"

            if ret.group(1) == "POST ":     # 这里还是有点问题，直接用于对比，可以使用正则匹配，防止小写，或者其他什么原因。
                if 'username' in repuest_lines[-1]:
                    post_ret = re.match(r"[^=]+=([^&]*)[^=]+=(.*)",repuest_lines[-1])
                    login_username = post_ret.group(1)
                    login_password = post_ret.group(2)
                    # 字典传入是否认证通过
                    login_true = login_username == self.useranme and login_password == self.userpassword
                else:
                    new_socket.setblocking(False)
                    data = b''
                    sleep(0.5)
                    try:
                        while True:
                            data += new_socket.recv(1024)
                    except socket.error as e:
                        # 当没有接收到数据时，报错并跳出循环
                        pass
                    file_option = data
            
            cookie_v = [re.match(r'Cookie: (.*)',i).group(1) for i in repuest_lines if 'Cookie' in i]
            if cookie_v:
                if cookie_v[0] == 'login_cookie':
                    login_true = True

        if  file_name.endswith(".html") or file_name.endswith(".md") or file_name.endswith(".php"):
            #使用伪静态，，，如果以 html 或者 md 结尾将数据导入框架来执行。。
            env = dict()
            #将数据处理传送到框架上来返回报文头与底
            #报文头由set_response_header处理
            #身体由函数返回

            #字典是传入需要处理的数据
            # 字典传入请求的文件名
            env['PATH_INFO'] = file_name
            # 字典传入系统访问资源的静态地址
            env['static_path'] = self.static_path
            # 字典传入操作
            env['login_true'] = login_true
            # 字典传入需要操作的内容
            env['file_option'] = file_option

            #body = WSGI_frame.application(env, self.set_response_header)
            body = self.application(env, self.set_response_header)

            header = "HTTP/1.1 %s\r\n" % self.status

            for temp in self.headers:
                header += "%s:%s\r\n" % (temp[0],temp[1])

            header += "\r\n"

            response = header + body 

            new_socket.send(response.encode("utf-8"))
        else:
            # 如何使用其他的文件方式访问，直接调用系统中的资源并直接返回
            # 排除异常
            try:
                # 访问系统资源是否存在，如何存在返回
                f=open(self.static_path + file_name,"rb")
            except:
                repuest = "HTTP/1.1 404 NOT FOUND\r\n"  # 返回表头
                repuest += "\r\n"
                repuest += "------file not found---------"
                new_socket.send(repuest.encode("utf-8"))
            else:
                html_content = f.read()
                f.close()
                repuest = "HTTP/1.1 200 OK\r\n"
                repuest += "\r\n"
                #发送hender
                new_socket.send(repuest.encode("utf-8"))
                #发送body
                new_socket.send(html_content)
        new_socket.close()

    def set_response_header(self,status,headers):
        self.status = status
        self.headers = headers

    def run(self):
        while True:
            new_socket , cliemt_addr=self.tcp_server_socket.accept()
            p = multiprocessing.Process(target = self.server_client, args=(new_socket,))
            p.start()
            new_socket.close()
        self.tcp_server_socket.close()


def main():

    with open("./web_server.conf", encoding="utf-8") as f:
        conf_info = eval(f.read())

    frame_name = conf_info["frame_name"]    # 使用的框架名
    app_name = conf_info["app_name"]        # 框架主函数名
    port = conf_info["port"]                # 开放端口

    # sys.path.append(conf_info['dynamic_path'])  # 设置可以调用模块的文件目录

    frame = __import__(frame_name)
    app = getattr(frame,app_name) #在模块中找app_name中的函数
    # print(app)
    
    web = WSGI_mini_web(port,app,conf_info['static_path'],conf_info['login_username'],conf_info['login_password'])
    web.run()

if __name__ == '__main__':
    main()

