import json


def extract_urls(path_json: str) -> list:
    urls = []
    with open(path_json, 'r') as f:
        entries = json.load(f)
        for entry in entries:
            urls.append(entry['url'])
    return urls


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Extracts the urls from a JSON file')
    parser.add_argument('in_file', metavar='IF', type=str, help='Input path to .json file')
    parser.add_argument('out_file', metavar='OF', type=str, help='Output path to .urls file')
    parser.add_argument('--prepend', type=str, help='Prepends text to the url')

    args = parser.parse_args()
    with open(args.out_file, 'w') as of:
        urls = extract_urls(args.in_file)
        prepend = '' if args.prepend is None else args.prepend
        of.write('\n'.join([prepend + url for url in urls]))
