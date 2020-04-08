import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from datetime import datetime

from const import URL_TEST


def run_link_check(url):
    now = datetime.now().strftime("%Y%m%d_%H%M")
    if url == URL_TEST:
        type_str = "test_page"
    else:
        type_str = f"prod_{re.search('/[^/]+/$', url)[0].replace('/', '')}"

    file_path = f"link_error_{type_str}_{now}.xlsx"
    print(url)
    r = _fetch_website(url)
    print(r.status_code)
    # print(re.sub("[\n\t]+", "", r.text.strip()))

    soup = BeautifulSoup(re.sub("[\n\t]+", "", r.text.strip()), "lxml")
    names = soup.find_all("h4")

    error_df = pd.DataFrame()
    for restaurant in names:
        try:
            links = restaurant.next_sibling.find_all("a")
            print(restaurant.text)
        except KeyError:
            pass
        else:
            for link in links:
                print(link.text)
                try:
                    print(link["href"])
                    r = _fetch_website(link["href"])
                except:
                    error_df = pd.concat(
                        [
                            error_df,
                            pd.DataFrame(
                                _create_error_dict(
                                    restaurant.text, link.text, link["href"], note="不正なURL"
                                )
                            ),
                        ]
                    )
                    print("Invalid URL!")
                    # pass
                else:
                    if r.status_code != 200:
                        error_df = pd.concat(
                            [
                                error_df,
                                pd.DataFrame(
                                    _create_error_dict(
                                        restaurant.text, link.text, link["href"], note="リンクエラー"
                                    )
                                ),
                            ]
                        )
                        print("Link doesn't work!")
                    else:
                        print("OK")

    error_df.reset_index(drop=True, inplace=True)
    # error_df

    error_df.to_excel(file_path)
    print("Exported!")

    return now, file_path, type_str


def _fetch_website(url):
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    return r


def _create_error_dict(name, link_type, url, note=None):
    error_dict = {"name": [name], "link_type": [link_type], "url": [url], "note": None}
    if note:
        error_dict["note"] = note
    return error_dict
