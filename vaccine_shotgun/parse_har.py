import argparse
import json


def parse_har(har_file):
    with open(har_file) as f:
        har_dict = json.load(f)

    for entry in har_dict['log']['entries']:
        url = entry['request']['url']
        if '/search_results/' in url:
            yield url


def main(har_file):
    for url in parse_har(har_file):
        print(url)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", default="doctolib.har")
    args = parser.parse_args()
    main(args.file)
