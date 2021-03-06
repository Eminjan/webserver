#!/usr/bin/python3
# -*-coding:utf-8 -*-
#Author:Eminjan
#@Time  :2018/5/13 11:36

import socket

# 服务端口

try:
    HttpPort = int(input('please input the server port,default port is 9420:'))
except Exception as e:
    HttpPort = 9420


# 地址信息
HttpHost = ('localhost',HttpPort)
# 返回的头部信息
HttpResponseHeader = '''HTTP/1.1 200 OK
Content-Type:text/html

'''
HttpResponseBody = ''
# 新的socket

ListenSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# 绑定监听

ListenSocket.bind(HttpHost)
ListenSocket.listen(100)

# 报头与报文分隔符
LineSeparator = '\r\n\r\n'

print('The server in running on port %d' % HttpPort)
print('The url is http://localhost:%d' % HttpPort)

# 获取请求报头

def get_headers(request):
    # 分隔符切割
    headers_arr = request.split('\r\n')
    # 第一行是请求方法方法 请求路径 HTTP协议版本
    headers = {}
    for item__ in headers_arr[1:]:
        item_ = item__.split(':')
        headers[item_[0]] = item_[1]
    return headers

# 获取POST表单参数
def get_post_args(request_body):
    post_args_arr = request_body.split('&')
    post_args = {}
    for item__ in post_args_arr:
        item_ = item__.split('=')
        post_args[item_[0]] = item_[1]
    return post_args

while True:
    HttpResponseBody = 'Hi :)'
    Client,Address = ListenSocket.accept()
    Request = Client.recv(1024).decode(encoding='utf-8')

    # 将用户请求分割为 报头，主体
    RequestText = Request.split(LineSeparator)
    RequestHeader = RequestText[0]
    RequestBody = RequestText[1]
    RequestMethod = RequestHeader.split(' ')[0]
    RequestUrl = RequestHeader.split(' ')[1]
    RequestHeaders = get_headers(RequestHeader)
    HttpResponseBody = ''
    print(Request)

# GET方法的处理
    if RequestMethod =='GET':
        HttpResponseBody += '<html>'
        HttpResponseBody += 'Your method is GET and your request url is ' + RequestUrl + '<br>'
        HttpResponseBody += 'Following are you headers :<br>********************************************<br>'

        for item in RequestHeaders.items():
            HttpResponseBody += ('<list>' + item[0] + ' => ' + item[1] + '</list><br>')
        HttpResponseBody += '<br><br>The next is post test <br>'


        HttpResponseBody += '''
        <form action="/" method="post">
        <p>Text1: <input type="text" name="Text1" /></p>
        <p>Text2: <input type="text" name="Text2" /></p>
        <input type="submit" value="Submit" />
        </form>
        '''

        HttpResponseBody += '</html>'

        # POST方法的处理
    elif RequestMethod == 'POST':
        HttpResponseBody += '<html>'
        HttpResponseBody += 'Your method is POST and your request url is ' + RequestUrl + '<br>'
        HttpResponseBody += 'Following are your headers :<br>********************************************<br>'
        for item in RequestHeaders.items():
            HttpResponseBody += ('<list>' + item[0] + ' => ' + item[1] + '</list><br>')
        HttpResponseBody += 'Following is your form :<br>********************************************<br>'
        PostArgs = get_post_args(RequestBody)
        for item in PostArgs.items():
            HttpResponseBody += ('<list>' + item[0] + ' => ' + item[1] + '</list><br>')
        HttpResponseBody += '<br><br>The next is get test <br>'
        HttpResponseBody += '<a href="http://' + RequestHeaders['Host'] + '/">get test</a>'
        HttpResponseBody += '</html>'

    else:
        HttpResponseBody += '<html>'
        HttpResponseBody += 'So sorry this method is not support :('
        HttpResponseBody += '</html>'

    Client.sendall((HttpResponseHeader+HttpResponseBody).encode(encoding='utf-8'))
    Client.close()

