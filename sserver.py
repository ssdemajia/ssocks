import socket
import select

"""
放在vps上
"""

SS_INIT = 1     # socks 5阶段
SS_ADDR = 2     # 获得地址
SS_TCP = 4
SS_DNS = 8
SS_UDP = 16


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setblocking(False)
s.bind(("", 9900))
s.listen(1024)
def main():
    rlist, wlist, elist = [s], [], []
    client_stage = {}
    tcp_headers = {}
    while True:
        readable, writable, errorable = select.select(rlist, wlist, elist)
        for fd in readable:
            if fd is s:  # 有新连接
                conn_fd, address = s.accept()
                conn_fd.setblocking(False)
                rlist.append(conn_fd)
                client_stage[conn_fd] = SS_ADDR
                print("connect client:", address)
            else:
                if client_stage[fd] == SS_ADDR:
                    pass
                    # ToDo


if __name__ == '__main__':
    main()