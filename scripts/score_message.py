#!/usr/bin/env python3
"""
Score a message against the BDR QA rules.

Usage:
    python scripts/score_message.py                    # Interactive mode
    python scripts/score_message.py "message text"     # Score inline
    python scripts/score_message.py --file msg.txt     # Score from file
    python scripts/score_message.py --batch file.json  # Score a batch
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.outbound_qa_engine import quick_score, score_batch_file


def main():
    if len(sys.argv) == 1:
        # Interactive mode
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
            print("\n" + quick_score(message))
        else:
            print("No message provided.")

    elif sys.argv[1] == "--file":
        path = sys.argv[2] if len(sys.argv) > 2 else None
        if not path or not os.path.exists(path):
            print(f"File not found: {path}")
            sys.exit(1)
        with open(path) as f:
            message = f.read().strip()
        print(quick_score(message))

    elif sys.argv[1] == "--batch":
        path = sys.argv[2] if len(sys.argv) > 2 else None
        if not path or not os.path.exists(path):
            print(f"File not found: {path}")
            sys.exit(1)
        print(score_batch_file(path))

    else:
        # Inline message
        message = " ".join(sys.argv[1:])
        print(quick_score(message))


if __name__ == "__main__":
    main()
