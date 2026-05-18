import hashlib
import hmac
import socket
import json
from datetime import datetime

SECRET_KEY = b"mysecretkey123"

def generate_hmac(message, timestamp):

    combined_data = f"{message}|{timestamp}"

    generated_hmac = hmac.new(
        SECRET_KEY,
        combined_data.encode(),
        hashlib.sha512
    ).hexdigest()

    return generated_hmac

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(("localhost", 7777))

server_socket.listen(1)

print("\nWaiting For Client...\n")

conn, addr = server_socket.accept()

packet = conn.recv(4096).decode()

packet_data = json.loads(packet)

print("\n---------------- NORMAL SERVER ----------------")

print("\nPacket Received Successfully")

received_message = packet_data["message"]
received_timestamp = packet_data["timestamp"]
received_hmac = packet_data["hmac"]

print("\nReceived Message:")
print(received_message)

print("\nReceived Timestamp:")
print(received_timestamp)

print("\nReceived HMAC:")
print(received_hmac)

server_generated_hmac = generate_hmac(
    received_message,
    received_timestamp
)

print("\nServer Generated HMAC:")
print(server_generated_hmac)

if server_generated_hmac == received_hmac:

    print("\nRESULT:")
    print("Authentication Successful")
    print("Access Granted")

else:

    print("\nAuthentication Failed")

conn.close()
