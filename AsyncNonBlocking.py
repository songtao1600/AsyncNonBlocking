'''
auth：songtao
异步非阻塞IO模块组件
'''
import socket
import select
import time
class HttpRequest(object):
    def __init__(self,sk,host,callback):
        self.socket = sk
        self.host = host
        self.callback = callback
    def fileno(self):
        return self.socket.fileno()

class HttpResponse(object):
    def __init__(self, recv_data):
        self.recv_data = recv_data
        self.header_dict = {}
        self.body = None

        self.initialize()
    def initialize(self):
        headers, body = self.recv_data.split(b'\r\n\r\n', 1)
        self.body = body
        header_list = headers.split(b'\r\n')
        for h in header_list:
            h_str = str(h, encoding='utf-8')
            v = h_str.split(':', 1)
            if len(v) == 2:
                self.header_dict[v[0]] = v[1]

class AsyncRequest(object):
    def __init__(self):
        self.read_list = []
        self.write_list = []
        self.error_list = []

    def add_request(self,host,callback):
        try:
            sk = socket.socket()
            sk.setblocking(0)
            sk.connect((host,80))
        except BlockingIOError as e:
            pass
        request = HttpRequest(sk,host,callback)
        self.read_list.append(request)
        self.write_list.append(request)
        # self.error_list.append(request)

    def run(self):
        while True:
            print(self.read_list,self.write_list,self.error_list)
            rlist, wlist, elist = select.select(self.read_list,self.write_list,self.error_list,0.05)

            for w in wlist:
                print(w.host,'链接成功.....')
                tpl = "GET / HTTP/1.0\r\nHost:%s\r\n\r\n"  %(w.host,)
                w.socket.send(bytes(tpl,encoding='utf-8'))
                self.write_list.remove(w)

            for r in rlist:

                recv_data = bytes()
                while True:
                    try:
                        chuch = r.socket.recv(2048)
                        recv_data += chuch
                        if len(chuch) < 2048:
                            break
                    except Exception as e:
                        break

                response = HttpResponse(recv_data)
                r.callback(response)

                r.socket.close()
                self.read_list.remove(r)

            if len(self.read_list) == 0:
                break

def f1(response):
    #回调处理函数
    pass
    # print('保存到文件',response)

def f2(response):
    # 回调处理函数
    pass
    # print('保存到数据库', response)

url_list = [
    {'host':'www.baidu.com','callback':f1},
    {'host':'cn.bing.com','callback': f2},
    # {'host':'www.cnblogs.com','callback': f2},
]

ar = AsyncRequest()
for url in url_list:
    ar.add_request(url['host'], url['callback'])

ar.run()

'''

class HttpRequest:
    def __init__(self,sk,host,callback):
        self.socket = sk
        self.host = host
        self.callback = callback
    def fileno(self):
        return self.socket.fileno()

class HttpResponse:
    def __init__(self,recv_data):
        self.recv_data = recv_data
        self.header_dict = {}
        self.body = None

        self.initialize()
    def initialize(self):
        headers, body = self.recv_data.split(b'\r\n\r\n', 1)
        self.body = body
        header_list = headers.split(b'\r\n')
        for h in header_list:
            h_str = str(h,encoding='utf-8')
            v = h_str.split(':',1)
            if len(v) == 2:
                self.header_dict[v[0]] = v[1]


class AsyncRequest:
    def __init__(self):
        self.conn = []
        self.connection = [] # 用于检测是否已经连接成功

    def add_request(self,host,callback):
        try:
            sk = socket.socket()
            sk.setblocking(0)
            sk.connect((host,80,))
        except BlockingIOError as e:
            pass
        request = HttpRequest(sk,host,callback)
        self.conn.append(request)
        self.connection.append(request)

    def run(self):

        while True:
            rlist,wlist,elist = select.select(self.conn,self.connection,self.conn,0.05)
            for w in wlist:
                print(w.host,'连接成功...')
                # 只要能循环到，表示socket和服务器端已经连接成功
                tpl = "GET / HTTP/1.0\r\nHost:%s\r\n\r\n"  %(w.host,)
                w.socket.send(bytes(tpl,encoding='utf-8'))
                self.connection.remove(w)
            for r in rlist:
                # r,是HttpRequest
                recv_data = bytes()
                while True:
                    try:
                        chunck = r.socket.recv(8096)
                        recv_data += chunck
                    except Exception as e:
                        break
                response = HttpResponse(recv_data)
                r.callback(response)
                r.socket.close()
                self.conn.remove(r)
            if len(self.conn) == 0:
                break

def f1(response):
    print('保存到文件',response.header_dict)

def f2(response):
    print('保存到数据库', response.header_dict)

url_list = [
    {'host':'www.baidu.com','callback': f1},
    # {'host':'cn.bing.com','callback': f2},
    {'host':'www.cnblogs.com','callback': f2},
]

req = AsyncRequest()
for item in url_list:
    req.add_request(item['host'],item['callback'])

req.run()

'''







