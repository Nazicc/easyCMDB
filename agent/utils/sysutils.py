#encoding: utf-8
# 存放生成uuid、获取主机名、ip地址、mac地址等的一些函数
# 
import uuid
import socket

def get_uuid():
    return str(uuid.uuid1()).replace('-', '')


def get_hostname():
    return socket.gethostname()


def get_ip_address():
    return socket.gethostbyname(socket.gethostname())


def get_mac_address():
    mac = uuid.UUID(int = uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e+2] for e in range(0,11,2)])
