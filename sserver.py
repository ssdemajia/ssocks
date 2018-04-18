import socket
import threading
import struct




def read(conn_fd):
    buffer = []
    while True:
        data = conn_fd.recv(4096)
        if not data:
            break
        else:
            print(data)
            buffer.append(data)
    buffer = ''.join(buffer)
    return buffer


def handler(conn_fd, addr):
    print("I'm in threading")
    data = read(conn_fd)
    ver = data[0]    # socks 版本
    nmethod = data[1]    # 客户端的支持方法个数

    if all(data[2:]):
        conn_fd.send(b'\x05\xff')
        return
    conn_fd.send(b'\x05\x00')




def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('192.168.178.120', 9998))
    s.listen(5)
    while True:
        conn_fd, address = s.accept()
        print("connect client:", address)
        try:
            threading.Thread(target=handler, args=(conn_fd, address)).start()
        except ConnectionResetError:
            print("Client close!!")


if __name__ == '__main__':
    main()