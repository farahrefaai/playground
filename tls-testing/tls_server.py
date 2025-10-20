import socket
import ssl


def create_tls_server(host='localhost', port=8443):
    # Create SSL context
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)

    # Load certificate and private key
    # You'll need to generate these files first (see instructions below)
    context.load_cert_chain('server.crt', 'server.key')

    # Optional: Configure security settings
    context.minimum_version = ssl.TLSVersion.TLSv1_2

    # Create TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)

    # Wrap socket with SSL
    secure_socket = context.wrap_socket(server_socket, server_side=True)

    print(f"TLS Server listening on {host}:{port}")

    try:
        while True:
            client_socket, addr = secure_socket.accept()
            print(f"Connection from {addr}")

            try:
                # Receive data
                data = client_socket.recv(1024).decode('utf-8')
                print(f"Received: {data}")

                # Send response
                response = f"Echo: {data}"
                client_socket.sendall(response.encode('utf-8'))
            except Exception as e:
                print(f"Error handling client: {e}")
            finally:
                client_socket.close()
    except KeyboardInterrupt:
        print("\nShutting down server...")
    finally:
        secure_socket.close()


if __name__ == "__main__":
    create_tls_server()