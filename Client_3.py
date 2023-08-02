import socket

UDP_IP = '127.0.0.3'  # Mengikat ke semua antarmuka jaringan yang tersedia
UDP_PORT = 5006

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.bind((UDP_IP, UDP_PORT))

print("Client siap untuk menerima data...")

while True:
    data, address = client_socket.recvfrom(1024)
    print(data.decode())
