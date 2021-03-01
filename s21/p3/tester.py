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

port = "5000"
page="Node_1.html"
address = f"http://localhost:{port}/{page}"
add=f"http://localhost:{port}/"
pass_bfs_file="MADCITY"
pass_dfs_file="COVID19"
password_bfs = "XÆ_A-12"
password_dfs = "BleuSus"

def FileScraper_go(fscraper):
    l1=fscraper.go("1")
    l4=fscraper.go("4")
    test=("".join(l1)!= "24") or ("".join(l4)!= "367")
    if test:
        print("unexpected go method for file scraper")
    return not(test)
def WebScraper_go(scraper):
    l1=[f"http://localhost:{port}/Node_{index}.html" for index in ["2","4"]]
    l4=[f"http://localhost:{port}/Node_{index}.html" for index in ["3","6","7"]]
    l1_exp=scraper.go(f"http://localhost:{port}/Node_1.html")
    test1=(l1!= l1_exp)
    l4_exp=scraper.go(f"http://localhost:{port}/Node_4.html")
    test2=(l4!=l4_exp)
    test=test1 or test2
    if test:
        print("unexpected go method for web scraper")
    return not(test)
    
def dfs_pass_file_test(fscraper):
    fscraper.dfs_search("1")
    rv="".join(fscraper.DFSorder)
    expected = pass_dfs_file
    if rv != expected:
        print(f"unexpected dfs pass: {repr(rv)}")
    return rv == expected

def bfs_pass_file_test(fscraper):
    fscraper.bfs_search("1")
    
    rv="".join(fscraper.BFSorder)
    #print(rv)
    expected = pass_bfs_file
    if rv != expected:
        print(f"unexpected bfs pass: {repr(rv)}")
    return rv == expected


def dfs_pass_test(scraper):
    rv = scraper.dfs_pass(address)
    expected = password_dfs
    if rv != expected:
        print(f"unexpected dfs pass: {repr(rv)}")
    return rv == expected

def bfs_pass_test(scraper):
    rv = scraper.bfs_pass(address)
    expected = password_bfs
    if rv != expected:
        print(f"unexpected bfs pass: {repr(rv)}")
    return rv == expected

def protected_df_test(scraper):
    points = 0

    # BFS
    df = scraper.protected_df(add,password_bfs)
    if df.iloc[0, -1] == "Picnic Point in Madison":
        points += 0.5
    else:
        print(f"did not expect {repr(df.iloc[0, -1])} in top-right cell for protected_df (BFS)")
    if len(df) == 8:
        points += 0.5
    else:
        print(f"did not expect {len(df)} rows for protected_df (BFS)")

    return points

def main():
    # load student code
    student_file_name=sys.argv[1] if len(sys.argv) > 1 else "scrape"
    imp.import_module(student_file_name)
    results = {"score": 0}
    score = 0
    
    #tests the revised part
    print("*** Testing GraphScraper and FileScraper ***\n")
    test_revised=[dfs_pass_file_test, bfs_pass_file_test,FileScraper_go]
    FScraper = imp.import_module(student_file_name).FileScraper
    
    for test_fn in test_revised:
        try:
            fscraper=FScraper()
            score = float(test_fn(fscraper))
            print(f"{test_fn.__name__} : {score} out of 1.0")
            results["score"] += score
            results[test_fn.__name__] = score
        except Exception as e:
            print("TEST EXCEPTION:", str(e))
            traceback.print_exc()
    
    
    # start server and test the web part 
    print("\n*** Testing WebScraper ***\n")
    Scraper = imp.import_module(student_file_name).WebScraper
    f = open("logfile.txt", "a") 
    p = Popen(["python3", "application.py", port], stdout=f, stderr=f, stdin=f)

    # start fresh browser/scraper
    os.system("pkill chrome")
    my_window=webdriver.Chrome(options=options)
    scraper = Scraper(my_window)


    tests= [WebScraper_go,dfs_pass_test, bfs_pass_test, protected_df_test,]


    for test_fn in tests:
        try:
            score=float(test_fn(scraper))
            results["score"] += score
            results[test_fn.__name__] = score
            print(f"{test_fn.__name__} : {score} out of 1.0")
        except Exception as e:
            print("TEST EXCEPTION:", str(e))
            traceback.print_exc()
    my_window.close()
    results["score"] *= 100 / (len(tests)+len(test_revised))

    with open("results.json", "w") as f:
        json.dump(results, f, indent=True)
    print("\n*** Final Results ***\n")
    print(results)
    p.kill()

if __name__ == "__main__":
    main()
