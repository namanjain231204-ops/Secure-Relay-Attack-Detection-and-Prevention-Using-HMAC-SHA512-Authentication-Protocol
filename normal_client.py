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

    return combined_data, generated_hmac

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect(("localhost", 7777))

print("\n---------------- NORMAL CLIENT ----------------")

message = "UNLOCK_DOOR"

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

combined_data, generated_hmac = generate_hmac(
    message,
    timestamp
)

print("\nOriginal Message:")
print(message)

print("\nTimestamp:")
print(timestamp)

print("\nCombined Data:")
print(combined_data)

print("\nGenerated HMAC:")
print(generated_hmac)

packet = {
    "message": message,
    "timestamp": timestamp,
    "hmac": generated_hmac
}

client_socket.send(json.dumps(packet).encode())

print("\nPacket Sent Successfully")

client_socket.close()
