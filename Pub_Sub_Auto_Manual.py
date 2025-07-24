import paho.mqtt.client as mqtt

broker = "broker.hivemq.com"
client_id = "pc_client"
temp_topic = "esp32/temp"
cmd_topic = "esp32/relay_cmd"
threshold_topic = "esp32/set_threshold"

def on_connect(client, userdata, flags, rc):
    print("Connected to broker")
    client.subscribe(temp_topic)

def on_message(client, userdata, msg):
    print(f"[ESP32] Temperature: {msg.payload.decode()} °C")

client = mqtt.Client(client_id)
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, 1883, 60)
client.loop_start()

while True:
    mode = input("\nChoose mode (manual/auto): ").strip().lower()

    if mode == "manual":
        while True:
            cmd = input("Type on/off/exit: ").strip().lower()
            if cmd == "exit":
                break
            if cmd in ["on", "off"]:
                client.publish(cmd_topic, cmd)

    elif mode == "auto":
        threshold = input("Enter temperature threshold: ")
        client.publish(threshold_topic, threshold)
        print("Auto mode active. Receiving temp data...")
