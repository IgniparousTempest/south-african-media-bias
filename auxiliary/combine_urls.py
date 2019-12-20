#!/usr/bin/env python3


def combine_urls(*files: list) -> list:
    urls = []
    for path in files:
        with open(path, 'r') as f:
            ls = f.readlines()
            for url in ls:
                url = url.rstrip('\n')
                urls.append(url)
    return list(set(urls))


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Combines url files into a single file with unique entries')
    parser.add_argument('in_files', metavar='IF', type=str, nargs='+', help='Input paths to .urls files')
    parser.add_argument('out_file', metavar='OF', type=str, help='Output path to .urls file')

    args = parser.parse_args()
    with open(args.out_file, 'w') as of:
        urls = combine_urls(*args.in_files)
        of.write('\n'.join(urls))
