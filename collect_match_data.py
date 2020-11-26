import argparse

from retrieve_matches import retrieve_matches
from get_match_data import get_match_data
import utils


def parse_arg():
    parser = argparse.ArgumentParser(description="Scrape Tennis Point-by-Point.")
    parser.add_argument("-d", "--directory", type=str, default=".", help="データを保存するディレクトリ")
    return parser.parse_args()


def main():
    args = parse_arg()
    print("Retrieving matches ... ", flush=True, end="")
    matches = retrieve_matches()
    print("done.")
    for match_name, match_href in matches:
        print("{} .".format(match_name), end="")
        data = get_match_data(match_href)
        print(".", end="")
        filename = utils.convert_to_safe_filename(match_name)
        print(".", end="")
        utils.save_match_data(data, args.directory, filename)
        print(" done.")


if __name__ == "__main__":
    main()
