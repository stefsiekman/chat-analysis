# Module to visualize how many messages are sent during each hour of the day

import argparse
import json
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description="Visualize how many messages were sent during each hour of the day.")
parser.add_argument("file", help="JSON messages file", type=argparse.FileType("r"))

args = parser.parse_args()

hours = [0] * 24

messages = [m for m in json.loads(args.file.read()) if m["text"] or m["media"]]
print(f"Loaded {len(messages)} messages.")

for message in messages:
    hour = int(message["time"][:2])
    hours[hour] += 1

plt.bar([x for x in range(24)], hours)
plt.ylabel("Message count")
plt.xticks([x for x in range(24)])
plt.title("Messages sent during each hour")
plt.show()

