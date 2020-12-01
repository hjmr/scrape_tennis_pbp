import argparse

import pandas as pd


def parse_arg():
    parser = argparse.ArgumentParser(description="Scrape Tennis Point-by-Point.")
    parser.add_argument("FILENAME", type=str, help="データのファイル名")
    return parser.parse_args()


def make_play_str(a_list):
    ret = ""
    if 1 < len(a_list):
        ret = "-".join([a_list[0], a_list[1]])
    else:
        ret = a_list[0]
    return ret


def proc_single_description(desc, result):
    records = [{}, {}]

    turn = 0
    for d in desc:
        d_str = make_play_str(d)
        turn = 0 if len(d) == 1 and "serve" in d[0] else 1 - turn
        if d_str not in records[turn]:
            records[turn][d_str] = 0
        records[turn][d_str] += 1

    win_lose_str = "Unknown"
    if result is None:
        print("Result is None.")
    elif "ace" in result or "winner" in result:
        win_lose_str = "Win" if turn == 0 else "Lose"
    elif "error" in result or "double fault" in result:
        win_lose_str = "Lose" if turn == 0 else "Win"
    else:
        print("Unexpected result: {}".format(result))

    return win_lose_str, records


def sum_up_single_data(data):
    players = []
    players = [p for p in data["Server"] if p not in players and not players.append(p)]
    if 2 < len(players):
        print("Unexpected condition: # of players = {}.".format(len(players)))

    records = {}
    for p in players:
        records[p] = {"Win": {"Count": 0}, "Lose": {"Count": 0}, "Unknown": {"Count": 0}}

    for idx in range(len(data)):
        row = data.iloc[idx]
        win_lose, rec = proc_single_description(row["Description"], row["Result"])

        server = row["Server"]
        server_win_lose = win_lose
        opponent = players[(players.index(server) + 1) % len(players)]
        opponent_win_lose = "Lose" if win_lose == "Win" else "Win"

        for i, p, w in [[0, server, server_win_lose], [1, opponent, opponent_win_lose]]:
            for k in rec[i]:
                if k not in records[p][w]:
                    records[p][w][k] = rec[i][k]
                else:
                    records[p][w][k] += rec[i][k]
            records[p][w]["Count"] += 1

    return records


if __name__ == "__main__":
    args = parse_arg()
    df = pd.read_json(args.FILENAME, orient="index", compression="infer")

    for i in range(len(df)):
        win_lose, rec = proc_single_description(df.iloc[i]["Description"], df.iloc[i]["Result"])
        print("[{}] Server: {} -> {}".format(i, df.iloc[i]["Server"], win_lose))

    result = sum_up_single_data(df)
    for player in result.keys():
        print("Player:{} {}-{}".format(player, result[player]["Win"]["Count"], result[player]["Lose"]["Count"]))
