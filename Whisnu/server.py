import os
import socket
import threading
import datetime


def handle_client(server_socket, client_address, data):
    choice, *message_parts = data.split(b'|')    
    # print(choice)
    # print(message_parts)
            
    if choice == b'1':
        destination_ip, destination_port, message = message_parts
        forward_message(choice, destination_ip, int(destination_port), message.decode('utf-8'), client_address[0], client_address[1])
    elif choice == b'2':
        # Handle pesan paragraf
        destination_ip, destination_port, paragraph_message = message_parts
        forward_message(choice, destination_ip, int(destination_port), paragraph_message.decode('utf-8'), client_address[0], client_address[1])
    elif choice == b'3':
        receive_file(server_socket, message_parts)
        # print('masuk keisni')


def main():
    server_ip = "127.0.0.1"
    server_port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((server_ip, server_port))
    print("UDP server berjalan...")

    while True:
        data, client_address = server_socket.recvfrom(65535)
        client_thread = threading.Thread(target=handle_client, args=(server_socket, client_address, data))
        client_thread.start()
            

def receive_file(server_socket, message_parts):
    chunk_size = 4096  # Ukuran chunk yang akan diterima    
    # Terima ukuran file dari klien
    data, client_address = server_socket.recvfrom(65535)

    now = datetime.datetime.now()
    timedate = now.strftime("%Y%m%d%H%M%S")
    file_size = int(message_parts[0].decode('utf-8'))
    file_name = message_parts[1].decode('utf-8')
    save_path = f'./storage/server/doc-pdf/{client_address[0]}-{client_address[1]}-{timedate}-{file_name}'
    print(f"Ukuran file yang akan diterima: {file_size} bytes")
    # print(f'{file_size}-{file_name}-{save_path}')

    # Terima file dan simpan dalam bentuk chunk
    received_size = 0
    with open(save_path, 'wb') as file:
        while received_size < file_size:
            chunk, _ = server_socket.recvfrom(chunk_size)
            file.write(chunk)
            received_size += len(chunk)

    print("File berhasil diterima dan disimpan.")

        
def forward_message(choice, destination_ip, destination_port, message, client_ip, client_port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    if(choice != 3):
        res = f'{choice}|Pesan dari {client_ip}:{client_port}|\n{message}'
        server_socket.sendto(res.encode('utf-8'), (destination_ip, destination_port))
        print(f"Pesan diteruskan ke {destination_ip}:{destination_port}")
    else:
        res = f'{choice}|Pesan dari {client_ip}:{client_port}|\n{message, " ini nomor 3"}'
        server_socket.sendto(res.encode('utf-8'), (destination_ip, destination_port))
        print(f"Pesan diteruskan ke {destination_ip}:{destination_port}")



if __name__ == "__main__":
    main()
