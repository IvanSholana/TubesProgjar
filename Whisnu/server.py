import os
import socket
from datetime import datetime

BUFFER_SIZE = 10240000

def main():
    server_ip = "127.0.0.1"
    server_port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((server_ip, server_port))
    print("UDP server berjalan...")

    while True:
        data, client_address = server_socket.recvfrom(BUFFER_SIZE)
        data = data.decode('utf-8')
        print(f"Pesan dari {client_address}: {data}")

        choice, *message_parts = data.split('|')
        if choice == '1':
            destination_ip, destination_port, message = message_parts
            forward_message(destination_ip, int(destination_port), message, client_address[0], client_address[1])
        elif choice == '2':
            # Handle pesan paragraf
            destination_ip, destination_port, paragraph_message = message_parts
            forward_message(destination_ip, int(destination_port), paragraph_message, client_address[0], client_address[1])
        elif choice == '3':
            destination_ip, destination_port, file_name, file_data = message_parts
            # handle_file_doc(destination_ip, int(destination_port), file_name, file_data, client_address[0], client_address[1])
            forward_file_doc(server_socket, destination_ip, int(destination_port), file_name, file_data, client_address[0], client_address[1])
        else:
            print("Pilihan tidak valid")
        
def forward_message(destination_ip, destination_port, message, client_ip, client_port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    res = f'Pesan dari {client_ip}:{client_port}\n{message}'
    server_socket.sendto(res.encode('utf-8'), (destination_ip, destination_port))
    print(f"Pesan diteruskan ke {destination_ip}:{destination_port}")

# def handle_file_doc(destination_ip, destination_port, file_name, file_data):
#     _, file_extension = file_name.split('.', 1)

#     if f".{file_extension.lower()}" not in ['.pdf', 'docx']:
#         print(f"File dengan ekstensi {file_extension} tidak diizinkan.")
#         return
    
#     # Buat nama file yang unik berdasarkan tanggal dan waktu saat ini
#     # current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
#     # new_file_name = f"{current_datetime}.{file_extension}"
    
#     # Path lengkap untuk menyimpan file
#     file_path = os.path.join('folder/doc', file_name)

#     # Simpan file yang diterima
#     with open(file_path, 'wb') as file:
#         file.write(file_data)

#     print(f"File '{file_name}' diterima dari {destination_ip}:{destination_port} dan disimpan di {file_path}.")
    
def forward_file_doc(destination_ip, destination_port, file_name, file_data, client_ip, client_port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Format pesan: "<choice>|<destination_ip>|<destination_port>|<file_data>"
    formatted_message = f"3|{destination_ip}|{destination_port}|{file_name}"

    # Kirim data dalam bentuk chunk ke client tujuan
    send_large_data(server_socket, destination_ip, destination_port, client_ip, client_port, formatted_message.encode('utf-8') + file_data)

    print(f"File '{file_name}' diteruskan ke {destination_ip}:{destination_port}")



def send_large_data(choice, server_socket, destination_ip, destination_port, client_ip, client_port, data):
    # Bagi data menjadi beberapa bagian (chunk)
    chunks = [data[i:i + 1024] for i in range(0, len(data), 1024)]

    # Kirim setiap chunk ke tujuan
    for i, chunk in enumerate(chunks):
        chunk_number = i + 1
        total_chunks = len(chunks)

        # Format pesan: "<chunk_number>|<total_chunks>|<chunk_data>"
        formatted_chunk = f"{choice}|{chunk_number}|{total_chunks}|{chunk}"

        server_socket.sendto(formatted_chunk.encode('utf-8'), (destination_ip, destination_port))

    # Kirim pesan penutup untuk menandai akhir pengiriman data
    res = f'Pesan dari {client_ip}:{client_port}\nSukses Mengirimkan File'
    server_socket.sendto(res.encode('utf-8'), (destination_ip, destination_port))
    print(f"Pesan diteruskan ke {destination_ip}:{destination_port}")

    
if __name__ == "__main__":
    main()
