import socket
import threading
import os
import datetime

data_clients = {
    1: {
        'ip' : '127.0.0.3',
        'port' : 12347
    }, 
    2 : {
        'ip' : '127.0.0.2', 
        'port' : 12346 
    }
}
 
def showClients():
     # Menggunakan loop for bersarang untuk mencetak semua key dan value
    for client_id, client_info in data_clients.items():
        print(f"Client ID: {client_id}\tIP: {client_info['ip']}\t Port:{client_info['port']}")

        
def main():
    server_ip = "127.0.0.1"
    server_port = 12345
    
    my_ip = '127.0.0.3'
    my_port = 12347

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    client_socket.bind((my_ip, my_port))

    print("UDP client berjalan...")

    send_thread = threading.Thread(target=send_message, args=(client_socket, server_ip, server_port))
    receive_thread = threading.Thread(target=receive_message, args=(client_socket,))

    receive_thread.daemon = True  # Menandai thread receive sebagai daemon, sehingga berhenti saat program utama berhenti.

    send_thread.start()
    receive_thread.start()
    
    send_thread.join()
    
    
    
def handle_msg_txt(choice, client_socket, server_ip, server_port):
    showClients()
    client_dest = int(input("Masukkan client_id tujuan: "))
    destination_ip = data_clients[client_dest]['ip']
    destination_port = data_clients[client_dest]['port']
    message = input("Masukkan pesan: ")

    # Format pesan: "<choice>|<destination_ip>|<destination_port>|<message>"
    formatted_message = f"{choice}|{destination_ip}|{destination_port}|{message}"
    client_socket.sendto(formatted_message.encode('utf-8'), (server_ip, server_port))
    print(f"Pesan terkirim ke {destination_ip}:{destination_port}")



def handle_msg_paragraph(choice, client_socket, server_ip, server_port):
    showClients()
    client_dest = int(input("Masukkan client_id tujuan: "))
    destination_ip = data_clients[client_dest]['ip']
    destination_port = data_clients[client_dest]['port']

    # Menerima inputan paragraf dari pengguna
    print("Masukkan pesan (ketik '.' di baris baru untuk mengakhiri):")
    message_lines = []
    while True:
        line = input()
        if line == '.':
            break
        message_lines.append(line)
    message = '\n'.join(message_lines)

    # Format pesan: "<choice>|<destination_ip>|<destination_port>|<message>"
    formatted_message = f"{choice}|{destination_ip}|{destination_port}|{message}"
    client_socket.sendto(formatted_message.encode('utf-8'), (server_ip, server_port))
    print(f"Pesan terkirim ke {destination_ip}:{destination_port}")
        
        

def send_message(client_socket, server_ip, server_port):
    while True:
        print("Pilih menu:")
        print("1. Kirim Pesan")
        print("2. Kirim Pesan Paragraph")  # Tambahkan pilihan ini
        print("3. Kirim File PDF/DOCX")
        print("0. Keluar")
        choice = input("Masukkan pilihan (0/1/2/3): ")

        if choice == '0':
            break
        elif choice == '1':
            handle_msg_txt(choice, client_socket, server_ip, server_port)
        elif choice == '2':  # Handle pilihan "Kirim Pesan Paragraph"
            handle_msg_paragraph(choice, client_socket, server_ip, server_port)
        elif choice == '3':
            file_path = input("Masukkan path file PDF/DOCX: ")
            if os.path.exists(file_path):
                send_file(choice, client_socket, server_ip, server_port, file_path)
            else:
                print("File tidak ditemukan.")

    client_socket.close()
   
    
#     print("File berhasil dikirim ke server.")
def send_file(choice, client_socket, server_ip, server_port, file_path):
    chunk_size = 4096  # Ukuran chunk yang akan dikirim
    file_size = os.path.getsize(file_path)

    init_msg = f'{choice}|{file_size}|{os.path.basename(file_path)}'
    # Kirimkan ukuran file ke server
    client_socket.sendto(init_msg.encode(), (server_ip, server_port))
    print("Ukuran file dikirim ke server.")

    # Baca dan kirim file dalam bentuk chunk
    with open(file_path, 'rb') as file:
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            client_socket.sendto(chunk, (server_ip, server_port))

    print(f"{file_path} berhasil dikirim.")


            
def receive_message(client_socket):
    while True:
        data, server_address = client_socket.recvfrom(1024)
        data = data.decode('utf-8')
        choice, recv_from, msg = data.split('|')
        print(f"{choice}\t{recv_from}\t{msg}")
        # print(f"\n{data}")

if __name__ == "__main__":
    main()
