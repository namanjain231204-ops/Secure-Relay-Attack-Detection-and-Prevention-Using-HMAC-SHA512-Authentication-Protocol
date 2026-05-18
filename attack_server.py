import hashlib
import hmac
import socket
import json
from datetime import datetime

# --------------------------------------------
# SECRET KEY
# --------------------------------------------

SECRET_KEY = b"mysecretkey123"

# --------------------------------------------
# GENERATE HMAC
# --------------------------------------------

def generate_hmac(message, timestamp):

    combined_data = f"{message}|{timestamp}"

    generated_hmac = hmac.new(
        SECRET_KEY,
        combined_data.encode(),
        hashlib.sha512
    ).hexdigest()

    return combined_data, generated_hmac

# --------------------------------------------
# SERVER SOCKET
# --------------------------------------------

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(("localhost", 8888))

server_socket.listen(1)

print("\nWaiting for Attacker/Client Connection...\n")

conn, addr = server_socket.accept()

print("Connected By:", addr)

packet = conn.recv(4096).decode()

packet_data = json.loads(packet)

print("\n---------------- SERVER SIDE ----------------")

received_message = packet_data["message"]
received_timestamp = packet_data["timestamp"]
received_hmac = packet_data["hmac"]

print("\nReceived Message:")
print(received_message)

print("\nReceived Timestamp:")
print(received_timestamp)

print("\nReceived HMAC:")
print(received_hmac)

current_time = datetime.now()

packet_time = datetime.strptime(
    received_timestamp,
    "%Y-%m-%d %H:%M:%S"
)

delay = (current_time - packet_time).total_seconds()

print("\nCurrent Server Time:")
print(current_time.strftime("%Y-%m-%d %H:%M:%S"))

print("\nPacket Delay:")
print(delay, "seconds")

print("\nGenerating HMAC Again Using:")
print(f"{received_message}|{received_timestamp}")

combined_data, server_generated_hmac = generate_hmac(
    received_message,
    received_timestamp
)

print("\nNew Server Generated HMAC:")
print(server_generated_hmac)

print("\nComparing HMACs...")

# --------------------------------------------
# VERIFY HMAC
# --------------------------------------------

if server_generated_hmac == received_hmac:

    if delay <= 5:

        print("\nRESULT:")
        print("Authentication Successful")
        print("Access Granted")

    else:

        print("\nRESULT:")
        print("Timestamp Expired")

        print("\nWARNING:")
        print("Relay Attack Detected")
        print("Packet Rejected")

else:

    print("\nRESULT:")
    print("HMAC MISMATCH DETECTED")

    print("\nWARNING:")
    print("Message Tampering Detected")
    print("Possible Relay Attack")
    print("Access Denied")

conn.close()
