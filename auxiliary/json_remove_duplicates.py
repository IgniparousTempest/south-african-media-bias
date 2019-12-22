#!/usr/bin/env python3
import json
from typing import List


def get_unique_entries(path_json: str) -> List[dict]:
    urls = []
    unique_entries = []
    with open(path_json, 'r') as f:
        entries = json.load(f)
        for entry in entries:
            if entry['url'] in urls:
                continue
            urls.append(entry['url'])
            unique_entries.append(entry)
    print(f'{len(unique_entries)} unique entries, removed {len(entries) - len(unique_entries)}.')
    return unique_entries


if __name__ == '__main__':
    import argparse
    import sys

    example_text = f"""example usage:
  {sys.argv[0]} times_live.json times_live.json
    """
    
    parser = argparse.ArgumentParser(description='Removes duplicate entries in a JSON file',
                                     epilog=example_text,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('in_file', metavar='IF', type=str, help='Input path to .json file')
    parser.add_argument('out_file', metavar='OF', type=str, help='Output path to .json file')

    args = parser.parse_args()

    entries = get_unique_entries(args.in_file)

    # Format the output file in the same manner as scrapy
    with open(args.out_file, 'w') as f:
        print('[', file=f)
        for i, entry in enumerate(entries):
            comma = ',' if i < len(entries) - 1 else ''
            string = json.dumps(entry)
            print(f'{string}{comma}', file=f)
        print(']', end='', file=f)
