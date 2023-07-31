import socket
# Inisialisasi socket UDP (Unicast)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ("localhost", 5000)

# Inisialisasi socket UDP (Multicast)
group = '224.1.1.1'
port = 5004
ttl = 2
sockMulti = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,socket.IPPROTO_UDP)
sockMulti.setsockopt(socket.IPPROTO_IP,socket.IP_MULTICAST_TTL,ttl)

sock.bind(server_address)
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
