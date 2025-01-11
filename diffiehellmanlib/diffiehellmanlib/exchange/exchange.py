import socket

def create_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return s

def server_bind_socket(ip:str, port:int, socket_object):
    socket_object.bind((ip, port))
    
def server_listen(socket_object):
    socket_object.listen(1)