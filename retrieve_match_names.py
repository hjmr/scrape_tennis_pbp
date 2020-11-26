import re

import requests
from bs4 import BeautifulSoup

import utils


def retrieve_match_names():
    res = requests.get(utils.base_url)
    soup = BeautifulSoup(res.text.encode(res.encoding), "html.parser")
    a_tags = soup.find_all("a", text=re.compile(r"^\d\d\d\d-\d\d-\d\d"))
    return [a.get_text().strip() for a in a_tags]


if __name__ == "__main__":
    match_names = retrieve_match_names()
    for n in match_names:
        print(n)
