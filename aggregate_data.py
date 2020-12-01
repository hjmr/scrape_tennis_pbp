import argparse

import pandas as pd

from sum_up_single_data import sum_up_single_data


def parse_arg():
    parser = argparse.ArgumentParser(description="Scrape Tennis Point-by-Point.")
    parser.add_argument("-c", "--csvfile", type=str, help="保存先のCSVファイル名")
    parser.add_argument("files", type=str, nargs="+", help="データのファイル名（複数指定可）")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arg()

    data = {}
    for f in args.files:
        df = pd.read_json(f, orient="index", compression="infer")
        sum_up = sum_up_single_data(df)
        for player in sum_up:
            dic = sum_up[player]
            for win_lose in dic:
                tag = "{}-{}".format(player, win_lose)
                if tag not in data:
                    data[tag] = {}
                for k in dic[win_lose]:
                    if k not in data[tag]:
                        data[tag][k] = 0
                    data[tag][k] += dic[win_lose][k]

    df = pd.DataFrame(data.values(), index=data.keys()).fillna(0.0)
    if args.csvfile is not None:
        df.to_csv(args.csvfile)
    else:
        print(len(df), len(df.columns))
