import argparse

from retrieve_match_names import retrieve_match_names
from get_match_data import get_match_data
import utils


def parse_arg():
    parser = argparse.ArgumentParser(description="Scrape Tennis Point-by-Point.")
    parser.add_argument("-d", "--directory", type=str, default=".", help="データを保存するディレクトリ")
    return parser.parse_args()


def main():
    args = parse_arg()
    match_names = retrieve_match_names()
    for match in match_names:
        print("{} .".format(match), end="")
        data = get_match_data(match)
        print(".", end="")
        filename = utils.convert_to_safe_filename(match)
        print(".", end="")
        utils.save_match_data(data, args.directory, filename)
        print(" done.")


if __name__ == "__main__":
    main()
