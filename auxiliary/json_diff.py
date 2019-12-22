#!/usr/bin/env python3
import json
from typing import List, Tuple


def are_json_entries_the_same(a: dict, b: dict) -> bool:
    if len(a.keys()) is not len(b.keys()):
        return False
    for k in a.keys():
        if a[k] is not b[k]:
            return False
    return True



def difference_between_json_files(json_path_a: str, json_path_b: str) -> Tuple[List[str], List[str], List[str], List[str]]:
    a: List[dict]
    b: List[dict]
    with open(json_path_a, 'r') as f:
        a = json.load(f)
    with open(json_path_b, 'r') as f:
        b = json.load(f)

    entries_in_common: List[str] = []
    entries_with_different_results: List[str] = []
    entries_only_in_a: List[str] = []
    entries_only_in_b: List[str] = []
    for entry in a:
        other = next((x for x in b if x['url'] == entry['url']), None)
        if other is not None:
            if are_json_entries_the_same(entry, other):
                entries_in_common.append(entry['url'])
            else:
                entries_with_different_results.append(entry['url'])
        else:
            entries_only_in_a.append(entry['url'])
    for entry in b:
        other = next((x for x in a if x['url'] == entry['url']), None)
        if other is None:
            entries_only_in_b.append(entry['url'])
    return entries_in_common, entries_with_different_results, entries_only_in_a, entries_only_in_b


if __name__ == '__main__':
    import argparse
    import sys

    example_text = f"""example usage:
  {sys.argv[0]} times_live.json times_live.json.old
    """

    parser = argparse.ArgumentParser(description='Determines the difference between two JSON files',
                                     epilog=example_text,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('file_a', metavar='A', type=str, help='First .json file')
    parser.add_argument('file_b', metavar='B', type=str, help='Second to .json file')

    args = parser.parse_args()
    common, different, only_a, only_b = difference_between_json_files(args.file_a, args.file_b)

    print(f'Files have the following number of entries:')
    print(f'  {len(common)} entries in common.')
    print(f'  {len(different)} entries with different results!')
    print(f'  {len(only_a)} entries only in the first file.')
    print(f'  {len(only_b)} entries only in the second file.')
