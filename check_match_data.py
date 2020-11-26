import argparse

import pandas as pd


def parse_arg():
    parser = argparse.ArgumentParser(description="Scrape Tennis Point-by-Point.")
    parser.add_argument("FILENAME", type=str, help="データのファイル名")
    return parser.parse_args()


def main():
    args = parse_arg()
    df = pd.read_json(args.FILENAME, compression="infer")
    print(df.iloc[-1])


if __name__ == "__main__":
    main()
