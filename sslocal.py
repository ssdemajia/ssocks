import socket
import select
import struct
from crypttest import rc4_crypt


SS_INIT = 1
SS_ADDR = 2
SS_TCP = 3
SS_DNS = 4
SS_UDP = 5
SS_WAIT_REMOTE = 6

client_stage = {}
tcp_headers = {}
remote_local = {}
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(False)    # 设置为非阻塞模式
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 地址重用
server.bind(('127.0.0.1', 9998))
server.listen(1024)
rlist, wlist, elist = [server], [], []


class SocksError(RuntimeError):
    def __init__(self, arg):
        self.args = arg


def handler_init(conn_fd):
    ver = conn_fd.recv(1)  # socks 版本
    nmethod = conn_fd.recv(1)  # 客户端的支持方法个数
    methods = conn_fd.recv(nmethod[0])  # ord()将 b'\x10' => 16
    print("1. {}|{}|{}".format(ver, nmethod, methods))
    if ord(ver) != 5:
        raise SocksError("用户没有使用版本5的socks")
    if all(methods):    # 说明有0x00这个方法
        conn_fd.send(b'\x05\xff')
        raise SocksError("用户没有使用0x00这个方法")
    conn_fd.send(b'\x05\x00')
    client_stage[conn_fd] = SS_ADDR


def handler_addr(conn_fd):
    ver = conn_fd.recv(1)  # 版本
    cmd = conn_fd.recv(1)  # command
    rsv = conn_fd.recv(1)
    atyp = conn_fd.recv(1)  # address type
    print("2. {}|{}|{}|{}".format(ver, cmd, rsv, atyp))
    if len(ver) != 1 or ver[0] != 5:
        raise SocksError('在addr中没有使用ver.5')
    if cmd[0] == 1:  # 表示tcp连接
        if atyp[0] == 1:  # ipv4 地址
            addr = conn_fd.recv(4)
            port = conn_fd.recv(2)
            dest_addr = socket.inet_ntop(socket.AF_INET, addr)
            dest_port = struct.unpack('>H', port)[0]
            length = 4
        elif atyp[0] == 3:    # 域名 后面会跟一个字节表示域名长度
            length = conn_fd.recv(1)   # 域名长度
            addr = conn_fd.recv(length[0])
            port = conn_fd.recv(2)
            dest_addr = addr
            dest_port = struct.unpack('>H', port)[0]
        else:
            print("Not ipv4 or domain!")
        print("{0}:{1}".format(addr, port))
        conn_fd.send(b"\x05\x00\x00\x01\x00\x00\x00\x00\x00\x00")
        tcp_headers[conn_fd] = (dest_addr, dest_port)
        client_stage[conn_fd] = SS_TCP
    elif cmd[0] == 3:  # udp连接
        raise SocksError("cmd udp:%d" % cmd[0])
    else:
        raise SocksError("cmd不认识:%d"%cmd[0])


def handler_tcp(conn_fd):
    """将数据加密后发往sserver"""
    data = conn_fd.recv(32 * 1024)
    print("tcp data:", len(data))
    remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_local[remote] = conn_fd
    client_stage[remote] = SS_WAIT_REMOTE
    remote.connect(("45.77.152.130", 9900))
    addr, port = tcp_headers[conn_fd]
    packet = bytes(len(addr)) + addr + port + data
    remote.send(rc4_crypt(b'shaoshuai', packet))
    rlist.append(remote)


def main():
    while True:
        readable, writable, errorable = select.select(rlist, wlist, elist)
        for fd in readable:
            if fd is server:   # 有新连接
                conn_fd, address = server.accept()
                conn_fd.setblocking(False)
                rlist.append(conn_fd)
                client_stage[conn_fd] = SS_INIT
                print("connect client:", address)
            else:
                if client_stage[fd] == SS_INIT:
                    handler_init(fd)
                elif client_stage[fd] == SS_ADDR:
                    handler_addr(fd)
                elif client_stage[fd] == SS_TCP:
                    handler_tcp(fd)


if __name__ == '__main__':
    main()