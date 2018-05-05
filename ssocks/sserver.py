import socket
import select
import struct
from ssocks.crypttest import rc4_crypt

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
    data = conn.recv(32*1024)
    # data = rc4_crypt(r"shaoshuai", data)
    len, port = struct.unpack("!HH", data[:4])
    addr_fmt = "!HH%ds" % len
    addr = struct.unpack(addr_fmt, data[:len+4])[2]
    data = data[len+4:]
    # print("请求地址为:", addr)
    # print("len:", len)
    remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(addr,port)
    remote.connect((addr, port))
    remote.send(data)
    recv_remote = remote.recv(32*1024)
    print(recv_remote)
    conn.send(recv_remote)
    conn.close()
    rlist.remove(conn)

def main():
    print("server open")
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