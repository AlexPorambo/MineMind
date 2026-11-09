import json
import websocket

# Connect Python to our Mineflayer bridge
ws = websocket.create_connection(
    "ws://127.0.0.1:8765",
    timeout=10
)

print("Connected to MineMind!")

def send_action(action):
    # Send a command to Minecraft
    command = {"action": action}

    ws.send(json.dumps(command))

    # Wait for Minecraft's response
    response = json.loads(ws.recv())

    if "error" in response:
        raise RuntimeError(response["error"])

    return response


# Read the bot's initial position
result = send_action("observe")
print("Starting position:", result["observation"])

# Test moving the character
actions = [
    "forward",
    "forward",
    "right",
    "jump",
    "back"
]

for action in actions:
    print(f"\nPerforming action: {action}")

    result = send_action(action)

    print("New position:", result["observation"])

ws.close()
print("\nTest complete!")
