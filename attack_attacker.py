import socket
import json
import time

# --------------------------------------------
# ATTACKER SERVER
# --------------------------------------------

attacker_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

attacker_server.bind(("localhost", 9999))

attacker_server.listen(1)

print("\nWaiting for Client Connection...\n")

client_conn, client_addr = attacker_server.accept()

print("Client Connected:", client_addr)

packet = client_conn.recv(4096).decode()

packet_data = json.loads(packet)

print("\n---------------- ATTACKER INTERCEPTION ----------------")

print("\nOriginal Packet Intercepted")

print("\nOriginal Packet:")
print(packet_data)

# --------------------------------------------
# MODIFY MESSAGE
# --------------------------------------------

print("\nAttacker Modifies Message...")

packet_data["message"] = "OPEN_GARAGE"

print("\nModified Message:")
print(packet_data["message"])

print("\nOld Timestamp:")
print(packet_data["timestamp"])

print("\nOld HMAC:")
print(packet_data["hmac"])

print("\nForwarding Tampered Packet To Server...")

# --------------------------------------------
# SEND TO SERVER
# --------------------------------------------

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.connect(("localhost", 8888))

modified_packet = json.dumps(packet_data)

time.sleep(2)

server_socket.send(modified_packet.encode())

server_socket.close()

client_conn.close()
