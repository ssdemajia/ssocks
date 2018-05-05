import socket
import select
from crypttest import rc4_crypt

"""
放在vps上
"""

SS_INIT = 1     # socks 5阶段
SS_ADDR = 2     # 获得地址
SS_TCP = 4
SS_DNS = 8
SS_UDP = 16


remote_local = {}
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setblocking(False)
s.bind(("", 9900))
s.listen(1024)
rlist, wlist, elist = [s], [], [s]
client_stage = {}
tcp_headers = {}


def handle_tcp(conn):
    data = conn.read(32*1024)
    data = rc4_crypt(r"shaoshuai", data)
    len = data[0]
    addr = data[1:len]
    print("请求地址为:",addr)

def main():
    while True:
        readable, writable, errorable = select.select(rlist, wlist, elist)
        for fd in readable:
            if fd is s:  # 有新连接
                conn_fd, address = s.accept()
                conn_fd.setblocking(False)
                rlist.append(conn_fd)
                client_stage[conn_fd] = SS_TCP
                print("connect client:", address)
            else:
                if client_stage[fd] == SS_TCP:
                    handle_tcp(fd)
        for fd in errorable:
            if fd is s:
                return

if __name__ == '__main__':
    main()