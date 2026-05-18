import hashlib
import hmac
import socket
from datetime import datetime
import json

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
# CLIENT SOCKET
# --------------------------------------------

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect(("localhost", 9999))

print("\n---------------- CLIENT SIDE ----------------")

message = "UNLOCK_DOOR"

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

print("\nOriginal Message:")
print(message)

print("\nTimestamp:")
print(timestamp)

combined_data, generated_hmac = generate_hmac(message, timestamp)

print("\nCombined Data:")
print(combined_data)

print("\nGenerated HMAC:")
print(generated_hmac)

packet = {
    "message": message,
    "timestamp": timestamp,
    "hmac": generated_hmac
}

packet_json = json.dumps(packet)

client_socket.send(packet_json.encode())

print("\nPacket Sent To Attacker/Server")

client_socket.close()
