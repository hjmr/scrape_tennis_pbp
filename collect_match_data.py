import re
import argparse

import requests
from bs4 import BeautifulSoup

import numpy as np
import pandas as pd


def parse_arg():
    parser = argparse.ArgumentParser(description="Scrape Tennis Point-by-Point.")
    parser.add_argument("-d", "--directory", type=str, default=".", help="データを保存するディレクトリ")
    return parser.parse_args()


def get_match_description(match):
    base_url = "http://www.tennisabstract.com/charting/"
    pointlog_str = "var pointlog = '"
    df = None
    res = requests.get(base_url)
    soup = BeautifulSoup(res.text.encode(res.encoding), "html.parser")
    a_link = soup.find("a", text=match)
    if a_link is not None:
        match_url = base_url + a_link["href"]
        res = requests.get(match_url)
        # pointlog の table 部分を抽出
        res_line = [s for s in res.text.split("\n") if s.startswith(pointlog_str)]
        if len(res_line) == 1:
            text = res_line[0][len(pointlog_str):-2]

            # pointlog の table 部分をパース
            soup = BeautifulSoup(text, "html.parser")
            cols = [th.get_text().strip() for th in soup.find_all("th")]
            cols[4] = "description"  # 4列目のタイトルが空なので適当につける
            content = [td.get_text().strip() for td in soup.find_all("td")]
            content = np.array(content).reshape(-1, len(cols))
            content = content[np.any(content != '', axis=1), :]  # 空行を削除
            df = pd.DataFrame(content, columns=cols)
    return df


def split_description(text):
    result = []
    text = re.sub(r"\(\d+-shot rally\)", "", text)
    paragraphs = [s.strip() for s in text.split(".") if 0 < len(s.strip())]
    for par in paragraphs:
        terms = [s.strip() for s in par.split(";") if 0 < len(s.strip())]
        if 1 < len(terms):
            result.extend([[x, y] for x, y in zip(terms[0:len(terms)-1], terms[1:len(terms)])])
        else:
            result.append(terms)
    return result


def get_match_data(match):
    df = get_match_description(match)
    for idx in range(len(df)):
        row = df.iloc[idx]
        row["description"] = split_description(row["description"])
    return df


def convert_to_safe_filename(text):
    return text.translate(str.maketrans(": ", "__"))


def main(directory):
    MATCH = "2020-11-22 Tour Finals F: Daniil Medvedev vs Dominic Thiem (ATP)"
    df = get_match_data(MATCH)
    filename = convert_to_safe_filename(MATCH)
    df.to_json(f"{directory}/{filename}", force_ascii=False, orient="index")


if __name__ == "__main__":
    args = parse_arg()
    main(args.directory)
