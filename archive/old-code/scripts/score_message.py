#!/usr/bin/env python3
"""
Score a message against the BDR QA rules.

Usage:
    python scripts/score_message.py                           # Interactive mode
    python scripts/score_message.py "message text"            # Score inline (Touch 1)
    python scripts/score_message.py --touch 2 "message text"  # Score as Touch 2
    python scripts/score_message.py --file msg.txt            # Score from file
    python scripts/score_message.py --batch file.json         # Score a batch
    python scripts/score_message.py --prospect '{"name":"..","company":".."}' "msg"
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.outbound_qa_engine import quick_score, score_batch_file


def main():
    args = sys.argv[1:]
    touch_number = 1
    prospect_json = ""
    message = None

    # Parse flags
    i = 0
    positional = []
    while i < len(args):
        if args[i] == "--touch" and i + 1 < len(args):
            try:
                touch_number = int(args[i + 1])
            except ValueError:
                print(f"Invalid touch number: {args[i + 1]}")
                sys.exit(1)
            i += 2
        elif args[i] == "--prospect" and i + 1 < len(args):
            prospect_json = args[i + 1]
            i += 2
        elif args[i] == "--file":
            if i + 1 >= len(args):
                print("Missing file path")
                sys.exit(1)
            path = args[i + 1]
            if not os.path.exists(path):
                print(f"File not found: {path}")
                sys.exit(1)
            with open(path) as f:
                message = f.read().strip()
            i += 2
        elif args[i] == "--batch":
            if i + 1 >= len(args):
                print("Missing batch file path")
                sys.exit(1)
            path = args[i + 1]
            if not os.path.exists(path):
                print(f"File not found: {path}")
                sys.exit(1)
            print(score_batch_file(path))
            return
        elif args[i] == "--help":
            print(__doc__)
            return
        else:
            positional.append(args[i])
            i += 1

    # If no message from --file, check positional args
    if message is None and positional:
        message = " ".join(positional)

    # Interactive mode if no message provided
    if message is None:
        print("Paste your message below (press Enter twice to score):\n")
        lines = []
        empty_count = 0
        try:
            while True:
                line = input()
                if line == "":
                    empty_count += 1
                    if empty_count >= 2:
                        break
                    lines.append(line)
                else:
                    empty_count = 0
                    lines.append(line)
        except EOFError:
            pass

        message = "\n".join(lines).strip()

    if message:
        print("\n" + quick_score(message, touch_number=touch_number,
                                 prospect_json=prospect_json))
    else:
        print("No message provided.")


if __name__ == "__main__":
    main()
