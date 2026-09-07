#!/usr/bin/env python3
"""Generate all 4-letter Discord username combinations using letters only."""

import itertools
import os
import argparse

ALPHABET = "abcdefghijklmnopqrstuvwxyz"


def generate_4_letter_usernames():
    return ("".join(chars) for chars in itertools.product(ALPHABET, repeat=4))


def main():
    parser = argparse.ArgumentParser(
        description="Generate all 4-letter usernames using letters only (no digits or symbols)."
    )
    parser.add_argument(
        "--output",
        default="4_letter_usernames.txt",
        help="Output file to save the generated usernames. Defaults to 4_letter_usernames.txt.",
    )
    parser.add_argument(
        "--count-only",
        action="store_true",
        help="Only print the total number of 4-letter combinations without writing the file.",
    )
    args = parser.parse_args()

    total = len(ALPHABET) ** 4
    print(f"Total 4-letter combinations: {total}")

    if args.count_only:
        return

    output_file = args.output
    with open(output_file, "w", encoding="utf-8") as f:
        for username in generate_4_letter_usernames():
            f.write(username + "\n")

    print(f"Generated {total} usernames and saved to {output_file} ({os.path.getsize(output_file) / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
