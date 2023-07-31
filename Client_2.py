# RECEIVER
import socket
import struct

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5004

# Multicast
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock.bind(('', MCAST_PORT))
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)

sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

# Broadcast
UDP_IP = '127.0.0.2'  # Mengikat ke semua antarmuka jaringan yang tersedia
UDP_PORT = 5006

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.bind((UDP_IP, UDP_PORT))


while True:
    # Multicast
    print(f"ini multicast : {sock.recv(10240)}")
    
    # Broadcast
    data, address = client_socket.recvfrom(1024)
    print(f"Menerima data dari {address}: {data.decode()}")