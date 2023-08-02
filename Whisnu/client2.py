import socket
import threading
import os
import datetime

BUFFER_SIZE = 10240000

    
def handle_msg_txt(choice, client_socket, server_ip, server_port):
    destination_ip = input("Masukkan alamat IP tujuan: ")
    destination_port = int(input("Masukkan port tujuan: "))
    message = input("Masukkan pesan: ")

    # Format pesan: "<choice>|<destination_ip>|<destination_port>|<message>"
    formatted_message = f"{choice}|{destination_ip}|{destination_port}|{message}"
    client_socket.sendto(formatted_message.encode('utf-8'), (server_ip, server_port))
    print(f"Pesan terkirim ke {destination_ip}:{destination_port}")

def handle_msg_paragraph(choice, client_socket, server_ip, server_port):
    destination_ip = input("Masukkan alamat IP tujuan: ")
    destination_port = int(input("Masukkan port tujuan: "))

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

def send_large_data(client_socket, server_ip, server_port, data):
    chunk_size = 1024  # Ukuran setiap chunk, misalnya 1024 byte (1KB)

    for i in range(0, len(data), chunk_size):
        chunk = data[i:i+chunk_size]

        # Format pesan: "<chunk_number>|<total_chunks>|<data_chunk>"
        formatted_message = f"{i//chunk_size + 1}|{len(data)//chunk_size}|{chunk}"
        client_socket.sendto(formatted_message.encode('utf-8'), (server_ip, server_port))

    # Kirim pesan akhir untuk menandakan semua chunk telah terkirim
    client_socket.sendto("END".encode('utf-8'), (server_ip, server_port))
        
def handle_msg_pdfOrDoc(choice, client_socket, server_ip, server_port):
    destination_ip = input("Masukkan alamat IP tujuan: ")
    destination_port = int(input("Masukkan port tujuan: "))
    file_path = input("Masukkan path file (DOCX/PDF): ")

    try:
        with open(file_path, 'rb') as file:
            file_data = file.read()
        # Format pesan: "<choice>|<destination_ip>|<destination_port>|<file_data>"
        # Dapatkan nama file dari path
        file_name = file_path.split('/')[-1]
        formatted_message = f"{choice}|{destination_ip}|{destination_port}|{file_name}"

        # Kirim data dalam bentuk chunk
        send_large_data(client_socket, server_ip, server_port, formatted_message.encode('utf-8') + file_data)

        print(f"File terkirim ke {destination_ip}:{destination_port}")
    except FileNotFoundError:
        print("File tidak ditemukan.")
    except Exception as e:
        print(f"Terjadi kesalahan saat mengirim file: {e}")
        

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
        elif choice == '3' :
            handle_msg_pdfOrDoc(choice, client_socket, server_ip, server_port)
            
    client_socket.close()


def receive_file(client_socket, file_path):
    with open(file_path, 'wb') as file:
        while True:
            data, server_address = client_socket.recvfrom(1024)
            if data == b"END":
                print(f"File diterima dan disimpan di {file_path}.")
                break
            file.write(data)
            
            
def receive_message(client_socket):
    while True:
        data, server_address = client_socket.recvfrom(BUFFER_SIZE)
        data = data.decode('utf-8')
        message_parts = data.split('|')

        if message_parts[0] == '3':  # Handle pilihan "Kirim File Dokumen"
            file_name = message_parts[3]
            file_path = os.path.join('client1/doc', file_name)

            receive_file(client_socket, file_path)
        else:
            print(f"\n{data}")

        
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

if __name__ == "__main__":
    main()
