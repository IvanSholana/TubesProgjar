# Client code
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

# Broadcast
UDP_IP = '127.0.0.1'  
UDP_PORT = 5006

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.bind((UDP_IP, UDP_PORT))

while True:
    # Unicast
    tujuan = int(input("Masukkan tujuan pesan: \n1.Server\n2.Client 2\n3.Client 3\nPilihan : "))
    if tujuan == 1:    
        message = input('Masukkan pesan: ')
        # Mengirim pesan ke server
        sock.sendto(message.encode(), server_address)
        # Menerima balasan dari server
        data, _ = sock.recvfrom(4096)
        print(f"ini unicast : {data.decode()}")
    elif tujuan == 2:
        message = input('Masukkan pesan: ')
        # Mengirim pesan ke server
        sock.sendto(f"{message},127.0.0.2".encode(), server_address)
    elif tujuan == 3:
        message = input('Masukkan pesan: ')
        # Mengirim pesan ke server
        sock.sendto(f"{message},127.0.0.3".encode(), server_address)
        
    # Multicast
    print(f"ini unicast : {sockMulti.recv(10240)}")
    
    # Broadcast
    data, address = client_socket.recvfrom(1024)
    print(f"Menerima data dari {address}: {data.decode()}")