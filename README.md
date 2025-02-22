# Team-Mechies-p2p-project

## Team Members
- **Saksham Gautam** (Roll No: 230003065)
- **Ishaan Sammi** (Roll No: 230003027)
- **Harsh Anand** (Roll No: 230005016)
- **Rohit Ranjan** (Roll No: 230003059)

## Project Overview
This project implements a network node that can:
- Accept incoming connections
- Establish outgoing connections to peers
- Send and receive messages
- Maintain and verify active peer connections
- Disconnect specific peers and shut down gracefully

## Running the Program
### Prerequisites
- Python 3.x installed
- A working network environment to establish peer-to-peer connections

### Installation
1. Clone this repository or download the script.
2. Open a terminal or command prompt in the project directory.

### Running the Node
To start a node:
```sh
python node.py <host> <port> [<peer_ip> <peer_port> ...]
```
- `<host>`: The IP address of the node
- `<port>`: The port number for the node
- `[<peer_ip> <peer_port> ...]` (optional): List of peer nodes to connect to initially

Example:
```sh
python node.py 127.0.0.1 5000
```
Or to connect to an existing node:
```sh
python node.py 127.0.0.1 5001 127.0.0.1 5000
```

### Commands
Once the program is running, the following commands can be used:
- `msg <message>` – Broadcasts a message to all connected peers.
- `add <peer_ip> <peer_port>` – Connects to a new peer.
- `remove <peer_ip> <peer_port>` – Disconnects from a peer.
- `verify <peer_ip> <peer_port>` – Checks if a peer connection is active.
- `show` – Displays all active connections.
- `exit` – Terminates the node and closes all connections.

## Bonus Question Handling
Our implementation **does handle** the bonus question by ensuring that the node establishes a connection with a sender if it's not already connected.

## Notes
- Ensure that firewalls and network configurations allow communication on the specified ports.
- The program should be terminated gracefully using the `exit` command or `Ctrl+C` to prevent connection issues.



