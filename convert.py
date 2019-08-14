# This module will convert a WhatsApp chat export file to JSON

import argparse
import json

parser = argparse.ArgumentParser(description="Convert WhatsApp data export to JSON.")
parser.add_argument("file", help="WhatsApp char export file to process", type=argparse.FileType("r", encoding="UTF-8"))
parser.add_argument("output", help="output JSON file, or stdout when empty", type=argparse.FileType("w", encoding="UTF-8"), nargs="?")

args = parser.parse_args()

class Message:

    def __init__(self, line):
        # Assertions in the line formatting
        assert ":" in line, line
        assert len(line) > 25, line

        # Extract information
        self.date = line[1:11]
        self.time = line[13:21]
        line = line[23:]
        colon_idx = line.find(":")
        self.sender = line[:colon_idx]
        self.message = line[colon_idx + 2:]

        self.non_text = self.message.startswith("\u200e")
        self.is_media = self.non_text and self.message.endswith("omitted")

    def append(self, line):
        self.message += "\n" + line

    def export(self):
        if not self.non_text:
            return json.dumps({
                "date": self.date,
                "time": self.time,
                "sender": self.sender,
                "text": not self.non_text,
                "media": False,
                "message": self.message,
            })
        else:
            return json.dumps({
                "date": self.date,
                "time": self.time,
                "sender": self.sender,
                "text": not self.non_text,
                "media": True,
            })


if args.output:
    args.output.write("[")
else:
    print("[", end="")


current_message = None
message_count = 0
for line in iter(args.file.readline, ""):
    # Strip the front and back
    line = line.strip(" \u200e\n")
    raw_line = line

    # Is this line the start of a new message?
    if line.startswith("["):
        # Process the last message, if there was any
        if current_message:
            if args.output:
                if message_count != 1:
                    args.output.write(",")
                args.output.write(current_message.export())
            else:
                print(current_message.export(), end="")

        current_message = Message(line)
        message_count += 1
    
    else:
        # Append to the existing message
        current_message.append(line)

args.file.close()

if args.output:
    args.output.write("]\n")
    args.output.close()
else:
    print("]")


print(f"The file had {message_count} messages")
