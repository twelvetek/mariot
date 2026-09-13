#!/usr/bin/env python3
import argparse
import signal
import sys
import time
import paho.mqtt.client as mqtt

parser = argparse.ArgumentParser(description="MQTT subscriber (paho)")
parser.add_argument("--host", default="127.0.0.1", help="MQTT broker host")
parser.add_argument("--port", type=int, default=1883, help="MQTT broker port")
parser.add_argument("--topic", default="test/salutation", help="Topic to subscribe to")
parser.add_argument("--qos", type=int, default=0, choices=[0,1,2], help="Subscription QoS")
args = parser.parse_args()

client = mqtt.Client(client_id="py-subscriber")

def on_connect(client, userdata, flags, rc):
    print(f"Connected to {args.host}:{args.port} (rc={rc})")
    client.subscribe(args.topic, qos=args.qos)
    print(f"Subscribed to topic: {args.topic} (qos={args.qos})")

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode("utf-8", errors="replace")
    except Exception:
        payload = str(msg.payload)
    print(f"[{msg.topic}] qos={msg.qos} payload={payload}")

client.on_connect = on_connect
client.on_message = on_message

def handle_sigint(sig, frame):
    print("Stopping subscriber...")
    client.disconnect()
    sys.exit(0)

signal.signal(signal.SIGINT, handle_sigint)

client.connect(args.host, args.port, keepalive=60)
client.loop_forever()