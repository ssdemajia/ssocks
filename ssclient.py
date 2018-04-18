import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("45.77.152.130", 8989))
buffer = []
s.send('\x05\x02\x00\x02'.encode())
while True:
    d = s.recv(1024)
    print(d)
    if d:
        buffer.append(d)
    else:
        break
data = ''.join(buffer)
print(data)