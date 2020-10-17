from selenium import webdriver 
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import pandas as pd
import numpy as np
import subprocess, traceback, sys, json
from subprocess import Popen
import importlib as imp
import os

options = Options()
options.headless = True

port = "5001"
address = f"http://localhost:{port}/"
password_bfs = "XÆ_A-12"
password_dfs = "BleuSus"

def easter_egg_test(scraper):
    rv = scraper.easter_egg()
    expected = "on wisconsin"
    #`onwisconsin` and `on wisconsin` are fine.
    if rv.replace(" ", "") != expected.replace(" ", ""):
        print(f"unexpected easter egg: {repr(rv)}")
    return rv.replace(" ", "") == expected.replace(" ", "")

def dfs_pass_test(scraper):
    rv = scraper.dfs_pass()
    expected = password_dfs
    if rv != expected:
        print(f"unexpected dfs pass: {repr(rv)}")
    return rv == expected

def bfs_pass_test(scraper):
    rv = scraper.bfs_pass()
    expected = password_bfs
    if rv != expected:
        print(f"unexpected bfs pass: {repr(rv)}")
    return rv == expected

def protected_df_test(scraper):
    points = 0

    # DFS
    df = scraper.protected_df(password_dfs)
    if df.iloc[0, -1] == "Gateway Arch in St.Louis":
        points += 0.25
    else:
        print(f"did not expect {repr(df.iloc[0, -1])} in top-right cell for protected_df (DFS)")
    if len(df) == 8:
        points += 0.25
    else:
        print(f"did not expect {len(df)} rows for protected_df (DFS)")

    # BFS
    df = scraper.protected_df(password_bfs)
    if df.iloc[0, -1] == "Picnic Point in Madison":
        points += 0.25
    else:
        print(f"did not expect {repr(df.iloc[0, -1])} in top-right cell for protected_df (BFS)")
    if len(df) == 8:
        points += 0.25
    else:
        print(f"did not expect {len(df)} rows for protected_df (BFS)")

    return points

def main():
    # load student code
    student_file_name=sys.argv[1] if len(sys.argv) > 1 else "scrape"
    imp.import_module(student_file_name)
    Scraper = imp.import_module(student_file_name).Scraper

    # start server
    f = open("logfile.txt", "a") 
    p = Popen(["python3", "application.py", port], stdout=f, stderr=f, stdin=f)

    # start fresh browser/scraper
    os.system("pkill chrome")
    my_window=webdriver.Chrome(options=options)
    scraper = Scraper(my_window, address)

    tests = [easter_egg_test, dfs_pass_test, bfs_pass_test, protected_df_test]
    results = {"score": 0}
    score = 0

    for test_fn in tests:
        try:
            score = float(test_fn(scraper))
            results["score"] += score
            results[test_fn.__name__] = score
        except Exception as e:
            print("TEST EXCEPTION:", str(e))
            traceback.print_exc()
    my_window.close()
    results["score"] *= 100 / len(tests)

    with open("results.json", "w") as f:
        json.dump(results, f, indent=True)
    print(results)
    p.kill()

if __name__ == "__main__":
    main()
