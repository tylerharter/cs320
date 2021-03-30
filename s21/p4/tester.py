import importlib
from bs4 import BeautifulSoup
import json
import os
import re
import sys
import time
import traceback
from collections import namedtuple
from datetime import datetime
from io import StringIO, BytesIO
from xml.etree import ElementTree as ET

import numpy as np
import pandas as pd

main_mod = None  # student's code
main_df = None  # student's data

################################nn########
# TEST FRAMEWORK
########################################

TestFunc = namedtuple("TestFunc", ["fn", "points"])
tests = []

# if @test(...) decorator is before a function, add that function to test_fucns
def test(points):
    def add_test(fn):
        tests.append(TestFunc(fn, points))

    return add_test


# override print so can also capture output for results.json
print_buf = None
orig_print = print


def print(*args, **kwargs):
    orig_print(*args, **kwargs)
    if print_buf != None:
        orig_print(*args, **kwargs, file=print_buf)


# both are simple name => val
# expected_json <- expected.json (before tests)
# actual_json -> actual.json (after tests)
#
# TIP: to generate expected.json, run the tests on a good
# implementation, then copy actual.json to expected.json
expected_json = None
actual_json = {}


def is_expected(actual, name, histo_comp=False):
    global expected_json

    actual_json[name] = actual
    if expected_json == None:
        with open("expected.json") as f:
            expected_json = json.load(f)

    expected = expected_json.get(name, None)

    # for hist_comp, we don't care about order of the two list like
    # objects.  We just care that the two histograms are similar.
    if histo_comp:
        if actual == None or expected == None:
            return "invalid histo_comp types: {}, {}".format(
                type(actual), type(expected)
            )

        if len(actual) != len(expected):
            return "expected {} points but found {} points".format(
                len(expected), len(actual)
            )
        diff = 0
        actual = sorted(actual)
        expected = sorted(expected)
        for a, e in zip(actual, expected):
            diff += abs(a - e)
        diff /= len(expected)
        if diff > 0.01:
            return "average error between actual and expected was %.2f (>0.01)" % diff

    elif type(expected) != type(actual):
        return "expected a {} but found {} of type {}".format(
            expected, actual, type(actual)
        )

    elif expected != actual:
        return "expected {} but found {}".format(expected, actual)

    return None


# execute every function with @test decorator; save results to results.json
def run_all_tests(mod_name="main"):
    global main_mod, main_df, print_buf
    print("Running tests...")

    main_mod = importlib.import_module(mod_name)
    main_path = mod_name + ".csv"
    main_df = pd.read_csv(main_path)
    if not 10 <= len(main_df.index) <= 1000:
        raise Exception("you must have between 10 and 1000 rows in ", main_path)
    if not 3 <= len(main_df.columns) <= 15:
        raise Exception("you must have between 3 columns and 15 columns in ", main_path)

    results = {
        "score": 0,
        "tests": [],
        "lint": [],
        "date": datetime.now().strftime("%m/%d/%Y"),
    }
    total_points = 0
    total_possible = 0

    t0 = time.time()
    for t in tests:
        print_buf = StringIO()  # trace prints
        print("=" * 40)
        print("TEST {} ({})".format(t.fn.__name__, t.points))
        try:
            points = t.fn()
        except Exception as e:
            print(traceback.format_exc())
            points = 0
        if points > t.points:
            raise Exception(
                "got {} points on {} but expected at most {}".format(
                    points, t.fn.__name__, t.points
                )
            )
        total_points += points
        total_possible += t.points
        row = {"test": t.fn.__name__, "points": points, "possible": t.points}
        if points != t.points:
            row["log"] = print_buf.getvalue().split("\n")
        results["tests"].append(row)
        print_buf = None  # stop tracing prints
        print("{} of {} points".format(points, t.points))

    print("=" * 40)
    print(
        "Earned {} of {} points across all tests".format(total_points, total_possible)
    )
    results["score"] = round(100.0 * total_points / total_possible, 1)

    # how long did it take?
    t1 = time.time()
    max_sec = 60
    sec = t1 - t0
    if sec > max_sec / 2:
        print("WARNING!  Tests took", sec, "seconds")
        print("Maximum is ", sec, "seconds")
        print("We recommend keeping runtime under half the maximum as a buffer.")
        print("Variability may cause it to run slower for us than you.")

    results["latency"] = sec

    # output results
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    with open("actual.json", "w", encoding="utf-8") as f:
        json.dump(actual_json, f, indent=2)

    print("=" * 40)
    print("SCORE: %.1f%% (details in results.json)" % results["score"])


########################################
# TESTS
########################################

# see https://en.wikipedia.org/wiki/Web_Server_Gateway_Interface#Example_of_calling_an_application
def app_req(path, expect_str=True, expect_errors=False, method="GET", input_body=""):
    errors = StringIO()

    parts = path.split("?")
    path = parts[0]
    query_string = ""
    if len(parts) > 1:
        query_string = parts[1]

    input_body = bytes(input_body, "utf-8")

    environ = {
        "REQUEST_METHOD": method,
        "PATH_INFO": path,
        "QUERY_STRING": query_string,
        "SERVER_NAME": "0.0.0.0",
        "SERVER_PORT": "3210",
        "SERVER_PROTOCOL": "HTTP/1.1",
        "wsgi.version": (1, 0),
        "wsgi.url_scheme": "http",
        "wsgi.input": BytesIO(input_body),
        "CONTENT_LENGTH": len(input_body),
        "wsgi.errors": errors,
        "wsgi.multithread": False,
        "wsgi.multiprocess": False,
        "wsgi.run_once": False,
    }

    status = None
    headers = None
    body = BytesIO()

    def start_response(rstatus, rheaders):
        nonlocal status, headers
        status, headers = rstatus, rheaders

    app_iter = main_mod.app.wsgi_app(environ, start_response)
    try:
        for data in app_iter:
            assert (
                status is not None and headers is not None
            ), "start_response() was not called"
            body.write(data)
    finally:
        if hasattr(app_iter, "close"):
            app_iter.close()

    errors = errors.getvalue()
    if errors and not expect_errors:
        print(errors)

    body = body.getvalue()
    if expect_str:
        body = str(body, "utf-8")
    return status, dict(headers), body


@test(points=10)
def has_pages():
    points = 0

    # Get SVG pages
    status, headers, body = app_req("/")
    page = BeautifulSoup(body, "lxml")
    svg_path_ll = page.find_all("img", src=re.compile("\S+.svg\S*"))
    svg_path_ll = [svg_path["src"] for svg_path in svg_path_ll]

    for link in ["/", "browse.html", "donate.html"]:
        status, headers, body = app_req(link)
        if status == "200 OK":
            points += 1
            page = BeautifulSoup(body, "lxml")
            if page.find_all(re.compile("^h[1-6]$")):
                points += 1
            else:
                print("page missing headers:", link)
        else:
            print("missing page:", link)

    svg_points = 0
    for link in svg_path_ll:
        status, headers, body = app_req(link)
        if status == "200 OK":
            svg_points += 1

    points += min(3, svg_points)

    status, headers, body = app_req("/missing.html", expect_errors=True)
    if status == "404 NOT FOUND":
        points += 1
    else:
        print("404 should be returned for a request to missing.html, but got", status)

    return points


@test(points=6)
def has_links():
    status, headers, body = app_req("/")
    page = BeautifulSoup(body, "lxml")
    links = page.find_all("a", href=True)
    links = [element["href"].split("?")[0] for element in links]
    points = 0
    for link in ["browse.html", "donate.html"]:
        if link in links:
            points += 3
        else:
            print(f"no hyperlink to {link} found on home page")
    return points


@test(points=20)
def browse():
    points = 0
    status, headers, body = app_req("/browse.html")
    dfs = pd.read_html(body)
    if len(dfs) == 1:
        points += 4
    else:
        print("browse.html should have exactly one table, but it had ", len(dfs))
        return 0

    df = dfs[0]
    if len(df) == len(main_df):
        points += 10
        eq = True
        for col in main_df.columns:
            if not col in df.columns:
                print("browse.html is missing column", col)
                eq = False
                break
            expected = df[col]
            actual = main_df[col]
            for i in range(len(expected)):
                if expected.iat[i] != actual.iat[i]:
                    dif_floats = (np.float64, np.float32, float)
                    if isinstance(expected.iat[i], dif_floats) and isinstance(
                        actual.iat[i], dif_floats
                    ):
                        if np.isnan(expected.iat[i]) and np.isnan(
                            actual.iat[i]
                        ):  # to check nans (they don't show as equal)
                            continue
                        elif round(expected.iat[i], 3) == round(
                            actual.iat[i], 3
                        ):  # round them and check
                            continue
                    elif isinstance(expected.iat[i], str) and isinstance(
                        actual.iat[i], str
                    ):  # something seems to enjoy randomly
                        if (
                            expected.iat[i].strip() == actual.iat[i].strip()
                        ):  # adding spaces in strings
                            continue
                        elif expected.iat[i].replace(" ", "") == actual.iat[i].replace(
                            " ", ""
                        ):
                            continue
                    err = "found {} but expected {} at row {} of column {}"
                    err = err.format(actual.iat[i], expected.iat[i], i, col)
                    print(err)
                    eq = False
                    break
            if not eq:
                break

        if eq:
            points += 6
    else:
        print(
            "the browse.html table should have {} rows, not {}".format(
                len(main_df), len(df)
            )
        )
    return points


@test(points=14)
def email():
    emails = {
        "user@example.com": True,
        "userATexample.com": False,
        "user@exampleDOTcom": False,
        "user123@gmail.com": True,
        "user@gmail@gmail.com": False,
    }

    if os.path.exists("emails.txt"):
        os.remove("emails.txt")

    points = 0
    n = 0
    for email, valid in emails.items():
        status, headers, body = app_req("/email", method="POST", input_body=email)
        if status != "200 OK":
            print("received status %s when trying to submit email" % status)
            return 0
        resp = json.loads(body)
        if valid:
            n += 1
            if resp.lower().find("thank") >= 0:
                points += 1
            else:
                print(
                    "response '%s' did not contain 'thank' for valid email '%s'"
                    % (resp, email)
                )

            if resp.lower().find(str(n)) >= 0:
                points += 1
            else:
                print(
                    "response '%s' did not contain correct 'n' for valid email '%s'"
                    % (resp, email)
                )
        else:
            if resp.lower().find("thank") >= 0:
                print(
                    "response '%s' contained 'thank' for invalid email '%s'"
                    % (resp, email)
                )
            else:
                points += 2

    if os.path.exists("emails.txt"):
        with open("emails.txt") as f:
            actual = {line.strip() for line in f}
            expected = {k for k in emails if emails[k]}
            if actual == expected:
                points += 4
            else:
                print(
                    "found emails {} in emails.txt, but expected {}".format(
                        actual, expected
                    )
                )
    else:
        print("no file emails.txt found")

    return points


def ab_test_helper(click_through=[], best=0):
    importlib.reload(main_mod)
    points = 0

    visits = 20  # how many times should we hit home page?
    learn = 10  # how many times does it try both before deciding?
    html = []  # HTML loaded from page for each visit

    for i in range(visits):
        status, headers, body = app_req("/")
        page = BeautifulSoup(body, "lxml")
        links = page.find_all("a", href=re.compile("donate.html\S*"))
        links = [link["href"] for link in links]
        if len(links) != 1:
            print("expected exactly one link to donate, but found", links)
            return 0
        if status != "200 OK":
            print("could not visit /")
            return 0

        html.append(body)

        if i in click_through:
            status, headers, body = app_req(links[0])
            if status != "200 OK":
                print("could not visit " + links[0])
                return 0

    # phase 1: alternate
    for i in range(1, learn):
        if html[i] == html[i - 1]:
            print("(a) did not alternate html in first %d visits" % learn)
            return points
        if i > 1 and html[i] != html[i - 2]:
            print("(b) did not alternate html in first %d visits" % learn)
            return points
    points += 1

    # phase 2: same
    for i in range(learn + 1, visits):
        if html[i] != html[i - 1]:
            print("did not consistently show same page after first %d visits" % learn)
            return points
    points += 2

    # did they choose the best for phase 2?
    if html[learn] != html[best]:
        print("did not choose the best version")
    else:
        points += 2

    return points


@test(points=30)
def ab_test():
    points = 0
    points += ab_test_helper(click_through=[0], best=0)
    points += ab_test_helper(click_through=[1], best=1)
    points += ab_test_helper(click_through=[0, 2, 4, 6, 8, 3, 5, 7, 9], best=0)
    points += ab_test_helper(click_through=[2, 4, 6, 8, 1, 3, 5, 7, 9], best=1)
    points += ab_test_helper(click_through=[2, 4, 6, 8, 5, 7, 9], best=0)
    points += ab_test_helper(click_through=[0, 6, 8, 3, 5, 7, 9], best=1)
    return points


@test(points=20)
def dashboard_examples():
    points = 0

    status, headers, body = app_req("/")

    ## Find list of svg's + their query string, then analyse
    page = BeautifulSoup(body, "lxml")
    svg_path_ll = page.find_all("img", src=re.compile("\S+.svg\S*"))
    svg_path_ll = [svg_path["src"] for svg_path in svg_path_ll]
    svg_set = set()

    if len(svg_path_ll) < 3:
        print(f"Expected atleast three SVGs, but found {len(svg_path_ll)} SVGs.")
        return points

    svg_route_ll = page.find_all("img", src=re.compile("(\S+?.svg)"))
    svg_route_set = set([route["src"].split("?")[0] for route in svg_route_ll])

    if len(svg_route_set) < 2:
        print(
            f"Expected atleast two unique routes, but found {len(svg_route_set)} routes."
        )
        return points

    num_valid_svg = 0
    for e, svg_path in enumerate(svg_path_ll):
        status, headers, body = app_req(svg_path)

        svg_set.add(body)

        # Save to temporary path
        fname = f"/tmp/svg_out_{e}.svg"
        with open(fname, "w") as f:
            f.write(body)

        doc = ET.parse(fname).getroot()
        # Check if XML is a SVG
        if "svg" not in doc.tag:
            print(f"{svg_path} doesn't seem to be a SVG.")
            continue
        else:
            num_valid_svg += 1

    if num_valid_svg >= 3:
        points += 20
    else:
        print(f"Atleast 3 unique SVGs required, only {len(num_valid_svg)} found.")
        points += 20 * num_valid_svg / 3

    return points


########################################
# RUNNER
########################################


def main():
    # import main.py (or other, if specified)
    mod_name = "main"
    if len(sys.argv) > 2:
        print("Usage: python3 test.py [mod_name]")
        sys.exit(1)
    elif len(sys.argv) == 2:
        mod_name = sys.argv[1]

    run_all_tests(mod_name)


if __name__ == "__main__":
    main()
