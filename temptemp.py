import socket
import threading
import sys
import time

class NetworkNode:
    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.connections = []
        self.active = True
        self.mutex = threading.Lock()
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.listener.bind((self.address, self.port))
        except Exception as e:
            print(f"[ERROR] Unable to bind to {self.address}:{self.port} - {e}")
            sys.exit(1)
        self.listener.listen(5)
        print(f"[INFO] Listening on {self.address}:{self.port}")

    def launch(self):
        thread = threading.Thread(target=self._accept_connections, daemon=True)
        thread.start()
        print("[INFO] Server is up and running.")

    def _accept_connections(self):
        while self.active:
            try:
                client, client_address = self.listener.accept()
                print(f"[INFO] Connection established with {client_address}")
                thread = threading.Thread(target=self._manage_client, args=(client, client_address), daemon=True)
                thread.start()
            except Exception as e:
                if self.active:
                    print(f"[ERROR] Connection handling error: {e}")

    def _manage_client(self, client, client_address):
        while self.active:
            try:
                data = client.recv(1024)
                if not data:
                    print(f"[INFO] Disconnected from {client_address}")
                    break
                received_msg = data.decode('utf-8')
                content, sender_ip, sender_port = received_msg.split("$%^&")
                print(f"[RECEIVED] From Team Mechies From {client_address}: {content}")
                if not self.connections:
                    self.initiate_connection(sender_ip, int(sender_port))
                else:
                    found = False
                    for conn in self.connections:
                        existing_ip, existing_port = conn.getpeername()
                        if existing_ip == sender_ip and existing_port == int(sender_port):
                            found = True
                            break
                    if not found:
                        self.initiate_connection(sender_ip, int(sender_port))
            except Exception as e:
                print(f"[ERROR] Communication error with {client_address}: {e}")
                break
        client.close()

    def initiate_connection(self, ip, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip, port))
            with self.mutex:
                self.connections.append(sock)
            print(f"[INFO] Connected to {ip}:{port}")
        except Exception as e:
            print(f"[ERROR] Failed to connect to {ip}:{port} - {e}")

    def broadcast_message(self, message):
        packaged_message = f"{message}$%^&{self.address}$%^&{self.port}"
        with self.mutex:
            for conn in self.connections:
                try:
                    conn.sendall(packaged_message.encode('utf-8'))
                    print(f"[SENT] by Team Mechies To {conn.getpeername()}: {message}")
                except Exception as e:
                    print(f"[ERROR] Failed to send message to {conn.getpeername()}: {e}")

    def verify_connection(self, ip, port):
        with self.mutex:
            for conn in self.connections:
                try:
                    if conn.getpeername() == (ip, port):
                        print(f"[INFO] Active connection with {ip}:{port}")
                        return True
                except Exception:
                    continue
        print(f"[WARNING] No active connection with {ip}:{port}")
        return False

    def show_connections(self):
        with self.mutex:
            if not self.connections:
                print("[INFO] No active connections.")
            else:
                print("[INFO] Active connections:")
                for conn in self.connections:
                    try:
                        print(f"  - {conn.getpeername()}")
                    except Exception as e:
                        print(f"  - [ERROR] Unable to retrieve connection info: {e}")

    def disconnect_peer(self, ip, port):
        with self.mutex:
            for conn in self.connections:
                try:
                    if conn.getpeername() == (ip, port):
                        conn.close()
                        self.connections.remove(conn)
                        print(f"[INFO] Disconnected from {ip}:{port}")
                        return
                except Exception as e:
                    print(f"[ERROR] Failed to disconnect {ip}:{port}: {e}")
            print(f"[WARNING] Connection with {ip}:{port} not found.")

    def shutdown(self):
        self.active = False
        self.listener.close()
        with self.mutex:
            for conn in self.connections:
                conn.close()
        print("[INFO] Node shutting down.")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python node.py <host> <port> [<peer_ip> <peer_port> ...]")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])
    node = NetworkNode(host, port)
    node.launch()
    time.sleep(1)

    if len(sys.argv) > 3:
        if (len(sys.argv) - 3) % 2 != 0:
            print("[ERROR] Incorrect peer format. Use pairs: <peer_ip> <peer_port>")
            sys.exit(1)
        for i in range(3, len(sys.argv), 2):
            peer_ip = sys.argv[i]
            peer_port = int(sys.argv[i + 1])
            node.initiate_connection(peer_ip, peer_port)

    try:
        while True:
            command = input("Enter command (msg/add/remove/show/verify/exit): ").strip()
            if not command:
                continue
            parts = command.split()
            action = parts[0].lower()

            if action == 'exit':
                break
            elif action == 'verify':
                if len(parts) != 3:
                    print("Usage: verify <peer_ip> <peer_port>")
                    continue
                node.verify_connection(parts[1], int(parts[2]))
            elif action == 'msg':
                if len(parts) < 2:
                    print("Usage: msg <message>")
                    continue
                node.broadcast_message(" ".join(parts[1:]))
            elif action == 'add':
                if len(parts) != 3:
                    print("Usage: add <peer_ip> <peer_port>")
                    continue
                node.initiate_connection(parts[1], int(parts[2]))
            elif action in ('remove', 'delete'):
                if len(parts) != 3:
                    print("Usage: remove <peer_ip> <peer_port>")
                    continue
                node.disconnect_peer(parts[1], int(parts[2]))
            elif action == 'show':
                node.show_connections()
            else:
                print("Invalid command. Use: msg, verify, exit")
    except KeyboardInterrupt:
        print("\n[INFO] Terminating...")

    node.shutdown()