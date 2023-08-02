# Server code
import socket

# Inisialisasi socket UDP (Unicast)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ("localhost", 5000)
sock.bind(server_address)

# Inisialisasi socket UDP (Multicast)
group = '224.1.1.1'
port = 5004
ttl = 2
sockMulti = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sockMulti.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

# Inisialisasi socket UDP (BroadCast)
CLIENT_1 = '127.0.0.4' 
CLIENT_2 = '127.0.0.2'  
CLIENT_3 = '127.0.0.3'  
UDP_PORT = 5006
broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    # Unicast
    print("Menunggu pesan dari client...")
    data, address = sock.recvfrom(4096)
    print(f"Menerima pesan dari client: {data.decode()}" )
    # Mengirim ke Client - Client
    if len(data.decode().split(',')) != 1:
        split_data = data.decode().split(',')
        message = split_data[0] 
        destination_ip = split_data[1] 
        broadcast_socket.sendto(f"{message}".encode(), (destination_ip, UDP_PORT))
    else:
        # Jika hanya menerima pesan unicast
        message = "Ini Pesan Unicast"
        sock.sendto(message.encode(), address)

        # Multicast
        sockMulti.sendto("Ini Pesan Multicast".encode('utf-8'), (group, port))

        # Broadcast
        broadcast_socket.sendto("Ini Pesan Broadcast".encode(), (CLIENT_1, UDP_PORT))
        broadcast_socket.sendto("Ini Pesan Broadcast".encode(), (CLIENT_2, UDP_PORT))
        broadcast_socket.sendto("Ini Pesan Broadcast".encode(), (CLIENT_3, UDP_PORT))