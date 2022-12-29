import socket

HOST = "127.0.0.1"
PORT = 8080


# index.html
def moveIndex(Client):
    header = """HTTP/1.1 301 Moved Permanently
Location: http://127.0.0.1:8080/index.html

"""
    Client.send(header.encode("utf-8"))


def sendIndex(Client):
    file = open("index.html", "rb")
    content = file.read()
    header = """HTTP/1.1 200 OK
Content-Length: %d

"""%len(content)
    header = header + content.decode()
    Client.send(header.encode("utf-8"))


def indexPage(Client, Server, Request):
    if "GET /index.html HTTP/1.1" in Request:
        sendIndex(Client)
        Server.close()
    elif "GET / HTTP/1.1" in Request:
        moveIndex(Client)
        Server.close()
        Server = createServer(HOST, PORT)
        Client, Request = readRequest(Server)
        print(Request)
        print("----------------------------------\n")
        indexPage(Client, Server, Request)


# 401.html
def send401(Client):
    file = open("401.html", "rb")
    content = file.read()
    header = """HTTP/1.1 200 OK
Content-Length: %d

"""%len(content)
    header = header + content.decode()
    Client.send(header.encode("utf-8"))


# 404.html
def move404(Server, Client):
    header = """HTTP/1.1 301 Moved Permanently
Location: http://127.0.0.1:8080/404.html

"""
    Client.send(header.encode("utf-8"))
    Server.close()


def send404(client):
    file = open("404.html", "rb")
    content = file.read()
    header = """HTTP/1.1 404 Not Found
Content-Type: text/html; charset=UTF-8
Content-Encoding: UTF-8
Content-Length: %d

""" % len(content)
    header += content.decode()
    client.send(header.encode("utf-8"))


def Page404(Server, Client):
    Server = createServer("localhost", PORT)
    Client, Request = readRequest(Server)
    # print("HTTP Request: ")
    # print(Request)
    if "GET /404.html HTTP/1.1" in Request:
        send404(Client)
    Server.close()


# info.html
def moveImage(Client):
    header = """HTTP/1.1 301 Moved Permanently
Location: http://127.0.0.1:8080/images.html

"""
    Client.send(header.encode("utf-8"))


def sendImage(Client):
    print("send Image")
    file = open("images.html", "rb")
    content = file.read()
    header = """HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8
Content-Encoding: UTF-8
Content-Length: %d

""" % len(content)
    header += content.decode()
    Client.send(header.encode("utf-8"))


def imagePage(Server, Client):
    print("Go to Image Page")
    Server.close()
    Server = createServer(HOST, PORT)
    Client, Request = readRequest(Server)
    print("HTTP Request: ")
    print(Request)
    if "GET /images.html HTTP/1.1" in Request:
        sendImage(Client)
    Server.close()


'''Create Serverrrrrrrrrrrrrrrrrrrrrrr'''
# socket(socket.AF_INET/socket.AF_INET6, SOCK_STREAM/SOCK_DGRAM)
# AF_INET: IPv4
# AF_INET: IPv6
# SOCK_STREAM: TCP
# SOCK_DGRAM: UDP


def createServer(host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(1)
    return server


def readRequest(Server):
    request = ""
    while request == "":
        client, address = Server.accept()
        print(str(address) + "connected")

        client.settimeout(1)
        try:
            temp = client.recv(1024).decode()
            while temp:
                request = request+temp
                temp = client.recv(1024).decode()

            # client.settimeout(None)
        except socket.timeout:
            print("time out")
    return client, request


# Check pass
def checkPass(Request):
    if "POST" in Request and "HTTP/1.1" in Request and "uname=admin&psw=123456" in Request:
        print("Login success")
        return True
    return False


if __name__ == "__main__":
    while True:
        server = createServer(HOST, PORT)
        client, request = readRequest(server)
        print(request)
        print("----------------------------------\n")
        indexPage(client, server, request)
        server.close()

        print(request)
        print("----------------------------------\n")
        loginSuccess = checkPass(request)
        if loginSuccess:
            # sendImage(client)
            moveImage(client)
            imagePage(server, client)
            # server.close()

            # server = createServer(HOST, PORT)
            # client, request = readRequest(server)
            #
            # imagePage(server, client, request)
        else:
            move404(server, client)
            Page404(server, client)

        # else:
        #     send401(client)
        #     server.close()
        # #     server = createServer(HOST, PORT)
        #     client, request = readRequest(server)
        #     print(request)
        #     print("----------------------------------\n")
        #     if clickedButton(request):
        #         moveFile(server, client)
        #         filePage(server, client)
        #         downloadPage()
        # else:
        #     move404(server, client)
        #     Page404(server, client)

