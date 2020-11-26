import argparse

import pandas as pd


def parse_arg():
    parser = argparse.ArgumentParser(description="Scrape Tennis Point-by-Point.")
    parser.add_argument("FILENAME", type=str, help="データのファイル名")
    return parser.parse_args()


def get_str(a_list):
    ret = ""
    if 1 < len(a_list):
        ret = "-".join([a_list[0], a_list[1]])
    else:
        ret = a_list[0]
    return ret


def sum_up_single_data(data):
    players = []
    players = [p for p in data["Server"] if p not in players and not players.append(p)]

    record = {}
    for p in players:
        record[p] = {"Points": 0}

    for idx in range(len(data)):
        row = data.iloc[idx]

        server_idx = players.index(row["Server"])
        turn = 0
        d_str = ""
        for d in row["Description"]:
            d_str = get_str(d)
            turn = 0 if "serve" in d_str else 1 - turn
            player_idx = (server_idx + turn) % 2
            if d_str not in record[players[player_idx]]:
                record[players[player_idx]][d_str] = 0
            record[players[player_idx]][d_str] += 1

        result = row["Result"]
        winner_idx = -1
        if result is None:
            print("Unexpected result: {}".format(result))
        elif "error" in result or "ace" in result:
            winner_idx = (server_idx + turn) % 2
        elif "winner" in result or "double fault" in result:
            winner_idx = (server_idx + turn + 1) % 2
        else:
            print("Unexpected result: {}".format(result))
        if 0 <= winner_idx:
            record[players[winner_idx]]["Points"] += 1

    return record


if __name__ == "__main__":
    args = parse_arg()
    df = pd.read_json(args.FILENAME, orient="index", compression="infer")
    result = sum_up_single_data(df)

    for player in result.keys():
        print("{}: {} ({})".format(player, result[player]["Points"], len(result[player].keys())-1))
