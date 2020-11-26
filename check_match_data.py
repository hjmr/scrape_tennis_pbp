import argparse

import pandas as pd


def parse_arg():
    parser = argparse.ArgumentParser(description="Scrape Tennis Point-by-Point.")
    parser.add_argument("-i", "--index", type=int, default=0, help="表示する行番号")
    parser.add_argument("FILENAME", type=str, help="データのファイル名")
    return parser.parse_args()


def main():
    args = parse_arg()
    df = pd.read_json(args.FILENAME, orient="index", compression="infer")
    if 0 <= args.index and args.index < len(df):
        print(df.iloc[args.index])
    else:
        print("Out of index (max = {})".format(len(df)-1))


if __name__ == "__main__":
    main()
