import socket
import threading
import struct
import logging

# def read(conn_fd):
#     buffer = b""
#     while True:
#         data = conn_fd.recv(4096)
#         if not data:
#             break
#         else:
#             # print(data)
#             buffer += data
#
#     return buffer


def handler(conn_fd, addr):
    print("I'm in threading")
    ver = conn_fd.recv(1)    # socks 版本
    nmethod = conn_fd.recv(1)    # 客户端的支持方法个数
    methods = conn_fd.recv(ord(nmethod))  # ord()将 b'\x10' => 16
    print("ver:", ver)
    if ord(ver) != 5:
        logging.error("用户没有使用版本5的socks")
    print("methods:", methods)
    if all(methods):    # 说明有0x00这个方法
        conn_fd.send(b'\x05\xff')
        return
    conn_fd.send(b'\x05\x00')
    ver = conn_fd.recv(1)   # 版本
    cmd = conn_fd.recv(1)   # command
    rsv = conn_fd.recv(1)
    atyp = conn_fd.recv(1)    # address type
    if ord(cmd) == 1:  # 表示tcp连接
        if ord(atyp) == 1:  # ipv4 地址
            dest_addr = socket.inet_ntop(socket.AF_INET, conn_fd.recv(4))
            dest_port = struct.unpack('>H', conn_fd.recv(2))[0]
        elif ord(atyp) == 3:    # 域名 后面会跟一个字节表示域名长度
            length = conn_fd.recv(1)   # 域名长度
            dest_addr = conn_fd.recv(ord(length))
            dest_port = struct.unpack('>H', conn_fd.recv(2))[0]
        else:
            print("Not ipv4 or domain!")
    elif ord(cmd) == 3:     # 建立udp连接
        print("UDP!")
    else:
        print("Not tcp or udp")




def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  #  地址重用
    s.bind(('127.0.0.1', 9998))
    s.listen(5)
    while True:
        conn_fd, address = s.accept()
        print("connect client:", address)
        # try:
        #     threading.Thread(target=handler, args=(conn_fd, address)).start()
        # except ConnectionResetError:
        #     print("Client close!!")
        handler(conn_fd, address)


if __name__ == '__main__':
    main()