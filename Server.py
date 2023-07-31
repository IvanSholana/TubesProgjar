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
UDP_IP = '127.0.0.3'  # Ganti dengan alamat IP tujuan unicast yang sesuai
UDP_PORT = 5006
broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    # Unicast
    print("Menunggu pesan dari client...")
    data, address = sock.recvfrom(4096)
    print("Menerima pesan dari client:", data.decode())
    # Mengirim balasan ke client
    message = "Ini Pesan Unicast"
    sock.sendto(message.encode(), address)

    # Multicast
    sockMulti.sendto("Ini Pesan Multicast".encode('utf-8'), (group, port))

    # Broadcast
    broadcast_socket.sendto("Ini Pesan Broadcast".encode(), (UDP_IP, UDP_PORT))