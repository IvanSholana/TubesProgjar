import socket
import os

def receive_file(save_path, host, port):
    chunk_size = 4096  # Ukuran chunk yang akan diterima

    # Inisialisasi socket UDP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))
    print("Menunggu koneksi dari klien...")

    # Terima ukuran file dari klien
    file_size, client_address = server_socket.recvfrom(8)
    file_size = int(file_size.decode())
    print(f"Ukuran file yang akan diterima: {file_size} bytes")

    # Terima file dan simpan dalam bentuk chunk
    received_size = 0
    with open(save_path, 'wb') as file:
        while received_size < file_size:
            chunk, _ = server_socket.recvfrom(chunk_size)
            file.write(chunk)
            received_size += len(chunk)

    print("File berhasil diterima dan disimpan.")
    server_socket.close()

if __name__ == "__main__":
    host = "127.0.0.10"  # Ganti dengan alamat IP server
    port = 33333  # Ganti dengan port yang sesuai
    save_path = "server-file/file_diterima.pdf"  # Ganti dengan lokasi dan nama file yang akan disimpan
    receive_file(save_path, host, port)
