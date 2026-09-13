#!/usr/bin/env python3
import argparse
import time
import threading
import paho.mqtt.client as mqtt

parser = argparse.ArgumentParser(description="MQTT publisher (paho)")
parser.add_argument("--host", default="127.0.0.1", help="MQTT broker host")
parser.add_argument("--port", type=int, default=1883, help="MQTT broker port")
parser.add_argument("--topic", default="test/salutation", help="Topic to publish to")
parser.add_argument("--message", default="Salut tout le monde.", help="Message payload")
parser.add_argument("--qos", type=int, default=0, choices=[0,1,2], help="Publish QoS")
parser.add_argument("--retain", action="store_true", help="Set retained flag")
args = parser.parse_args()

client = mqtt.Client(client_id="py-publisher")

publish_event = threading.Event()

def on_connect(client, userdata, flags, rc):
    print(f"Connected to {args.host}:{args.port} (rc={rc})")
    # publish once connected
    info = client.publish(args.topic, args.message.encode("utf-8"), qos=args.qos, retain=args.retain)
    # if qos > 0 we can wait for the mid to be published
    if args.qos == 0:
        print(f"Published (qos=0) to {args.topic}: {args.message}")
        publish_event.set()
    else:
        # info.mid is set; wait for on_publish
        print(f"Publishing (qos={args.qos}) to {args.topic}: {args.message}")

def on_publish(client, userdata, mid):
    print(f"Publish acknowledged (mid={mid})")
    publish_event.set()

client.on_connect = on_connect
client.on_publish = on_publish

client.connect(args.host, args.port, keepalive=60)
client.loop_start()

# wait for publish ack (or immediate for qos=0)
if not publish_event.wait(timeout=5):
    print("Warning: publish not acknowledged within timeout.")