import socket

UDP_IP = "10.1.1.3"
UDP_PORT = 5000
MESSAGE = 'take photo'
bufferSize = 1024

bytestosend = MESSAGE.encode('utf-8')

print("UDP target IP: %s" % UDP_IP)
print("UDP target port: %s" % UDP_PORT)
print("message: %s" % MESSAGE)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock.sendto(bytestosend, (UDP_IP, UDP_PORT))

data, addr = sock.recvfrom(bufferSize)

print('Data from server: ', data)