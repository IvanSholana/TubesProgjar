import socket
import os

def send_file(filename, host, port):
    chunk_size = 4096  # Ukuran chunk yang akan dikirim
    file_size = os.path.getsize(filename)

    # Inisialisasi socket UDP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Kirimkan ukuran file ke server
    client_socket.sendto(str(file_size).encode(), (host, port))
    print("Ukuran file dikirim ke server.")

    # Baca dan kirim file dalam bentuk chunk
    with open(filename, 'rb') as file:
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            client_socket.sendto(chunk, (host, port))

    print(f"{filename} berhasil dikirim.")
    client_socket.close()

if __name__ == "__main__":
    host = "127.0.0.10"  # Ganti dengan alamat IP server
    port = 33333  # Ganti dengan port yang sesuai
    filename = "../1.pdf"  # Ganti dengan nama file yang ingin dikirim
    send_file(filename, host, port)
