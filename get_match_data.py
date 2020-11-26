import re
import argparse

import requests
from bs4 import BeautifulSoup

import numpy as np
import pandas as pd

import utils


def retrieve_data_by_name(match_name):
    df = None
    res = requests.get(utils.base_url)
    soup = BeautifulSoup(res.text.encode(res.encoding), "html.parser")
    a_link = soup.find("a", text=match_name)
    if a_link is not None:
        df = retrieve_data_by_href(a_link["href"])
    return df


def retrieve_data_by_href(match_href):
    df = None
    pointlog_str = "var pointlog = '"
    match_url = utils.base_url + match_href
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
    df = None
    if match.endswith("html"):
        df = retrieve_data_by_href(match)
    else:
        df = retrieve_data_by_name(match)

    for idx in range(len(df)):
        row = df.iloc[idx]
        row["description"] = split_description(row["description"])
    return df


def parse_arg():
    parser = argparse.ArgumentParser(description="Scrape Tennis Point-by-Point.")
    parser.add_argument("-d", "--directory", type=str, default=".", help="データを保存するディレクトリ")
    return parser.parse_args()


if __name__ == "__main__":
    MATCH = "2020-11-22 Tour Finals F: Daniil Medvedev vs Dominic Thiem (ATP)"
    args = parse_arg()
    df = get_match_data(MATCH)
    fn = utils.convert_to_safe_filename(MATCH)
    utils.save_match_data(df, args.directory, fn)
