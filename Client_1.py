import socket
import struct


# Inisialisasi socket UDP Unicast
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 5000)

# Inisialisasi socket UDP Multicast
MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5004

sockMulti = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sockMulti.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sockMulti.bind(('', MCAST_PORT))
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)

sockMulti.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)


while True:
    # Unicast
    message = input('Masukkan pesan: ')
    # Mengirim pesan ke server
    sock.sendto(message.encode(), server_address)
    # Menerima balasan dari server
    data, _ = sock.recvfrom(4096)
    print('Menerima balasan dari server:', data.decode())
    
    # Multicast
    print(sockMulti.recv(10240))

    
