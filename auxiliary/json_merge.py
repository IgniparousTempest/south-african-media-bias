#!/usr/bin/env python3
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Needed to get 'auxiliary' module.

import json
import warnings
from typing import List

from auxiliary.json_diff import difference_between_json_files
from auxiliary.json_remove_duplicates import print_json_in_scrapy_style


def merge_json_files(json_path_a: str, json_path_b: str, keys_in_a: List[str], keys_in_b: List[str]) -> List[dict]:
    a: List[dict]
    b: List[dict]
    with open(json_path_a, 'r') as f:
        a = json.load(f)
    with open(json_path_b, 'r') as f:
        b = json.load(f)

    output = []
    for k in keys_in_a:
        entry = next((x for x in a if x['url'] == k))
        output.append(entry)
    for k in keys_in_b:
        entry = next((x for x in b if x['url'] == k))
        output.append(entry)
    return output


if __name__ == '__main__':
    import argparse

    example_text = f"""example usage:
  {sys.argv[0]} times_live.json times_live.json.old times_live.json

Caveats:
  * If json files have entries with differing values, the entries in the first file are used.
    """

    parser = argparse.ArgumentParser(description='Combines multiple .json files into one',
                                     epilog=example_text,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('file_a', metavar='A', type=str, help='Input path to first .json file')
    parser.add_argument('file_b', metavar='B', type=str, help='Input path to second .json file')
    parser.add_argument('out_file', metavar='OF', type=str, help='Output path to .json file')

    args = parser.parse_args()
    common, different, only_a, only_b = difference_between_json_files(args.file_a, args.file_b)
    if len(different) > 0:
        warnings.warn("Warning! The files have entries for the same URL that have different values!")

    entries = merge_json_files(args.file_a, args.file_b, common + different + only_a, only_b)
    print_json_in_scrapy_style(args.out_file, entries)
