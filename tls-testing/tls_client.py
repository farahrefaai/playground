import socket
import ssl
import os


def create_tls_client_with_keylog(host='localhost', port=8443, message='Hello, TLS Server!'):
    # Enable session key logging (for debugging only!)
    keylog_file = os.path.abspath("sslkeylog.txt")

    # Set environment variable if not already set
    if 'SSLKEYLOGFILE' not in os.environ:
        os.environ['SSLKEYLOGFILE'] = keylog_file

    print(f"Session keys will be logged to:")
    print(f"  {keylog_file}")
    print(f"\nCopy this path for Wireshark:")

    # Create SSL context
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)

    # Set the keylog callback (Python 3.8+)
    # This writes session keys to the file
    try:
        keylogfile = open(keylog_file, 'a')
        context.keylog_filename = keylog_file
        print(f"✓ Key logging enabled")
    except AttributeError:
        print("Note: keylog_filename requires Python 3.8+")
        print("Using SSLKEYLOGFILE environment variable instead")

    # For self-signed certificates
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    # Optional: Set minimum TLS version
    context.minimum_version = ssl.TLSVersion.TLSv1_2

    # Create TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Wrap socket with SSL
    secure_socket = context.wrap_socket(client_socket, server_hostname=host)

    try:
        # Connect to server (session keys generated here!)
        secure_socket.connect((host, port))
        print(f"\n✓ Connected to {host}:{port}")

        # Display connection info
        cipher = secure_socket.cipher()
        print(f"✓ Using cipher: {cipher[0]}")
        print(f"✓ TLS version: {secure_socket.version()}")

        # Get session info
        session = secure_socket.session
        if session:
            import binascii
            session_id = binascii.hexlify(session.id).decode()
            print(f"✓ Session ID: {session_id[:32]}...")

        # Send data
        secure_socket.sendall(message.encode('utf-8'))
        print(f"\n→ Sent: {message}")

        # Receive response
        response = secure_socket.recv(1024).decode('utf-8')
        print(f"← Received: {response}")

        print(f"\n{'=' * 60}")
        print(f"Session keys have been logged to: {keylog_file}")
        print(f"You can use this file with Wireshark to decrypt TLS traffic")
        print(f"{'=' * 60}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        secure_socket.close()
        if 'keylogfile' in locals():
            keylogfile.close()


def display_keylog_content():
    """Display the contents of the keylog file"""
    keylog_file = os.path.abspath("sslkeylog.txt")
    if os.path.exists(keylog_file):
        print(f"\n{'=' * 60}")
        print(f"KEYLOG FILE LOCATION:")
        print(f"  {keylog_file}")
        print(f"{'=' * 60}")
        print(f"CONTENTS:")
        print(f"{'=' * 60}")
        with open(keylog_file, 'r') as f:
            content = f.read()
            if content:
                print(content)
            else:
                print("(File is empty - keys not logged yet)")
        print(f"{'=' * 60}\n")


if __name__ == "__main__":
    print("WARNING: Session key logging enabled!")
    print("This is for LOCAL DEBUGGING ONLY - NEVER use in production!\n")

    try:
        create_tls_client_with_keylog()
        display_keylog_content()
    except ConnectionRefusedError:
        print("\nError: Could not connect to server.")
        print("Make sure the TLS server is running first!")