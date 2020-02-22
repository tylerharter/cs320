import importlib, sys, json, io, time, traceback, itertools
from datetime import datetime, timedelta
from collections import namedtuple
from matplotlib import pyplot as plt
from io import StringIO, BytesIO
from bs4 import BeautifulSoup
import pandas as pd

main_mod = None # student's code
main_df = None # student's data

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
            return ("invalid histo_comp types: {}, {}".format(type(actual), type(expected)))
        
        if len(actual) != len(expected):
            return "expected {} points but found {} points".format(len(expected), len(actual))
        diff = 0
        actual = sorted(actual)
        expected = sorted(expected)
        for a, e in zip(actual, expected):
            diff += abs(a - e)
        diff /= len(expected)
        if diff > 0.01:
            return "average error between actual and expected was %.2f (>0.01)" % diff

    elif type(expected) != type(actual):
        return "expected a {} but found {} of type {}".format(expected, actual, type(actual))

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

    results = {'score':0, 'tests': [], 'lint': [], "date":datetime.now().strftime("%m/%d/%Y")}
    total_points = 0
    total_possible = 0

    t0 = time.time()
    for t in tests:
        print_buf = StringIO() # trace prints
        print("="*40)
        print("TEST {} ({})".format(t.fn.__name__, t.points))
        try:
            points = t.fn()
        except Exception as e:
            print(traceback.format_exc())
            points = 0
        if points > t.points:
            raise Exception("got {} points on {} but expected at most {}".format(points, t.fn.__name__, t.points))
        total_points += points
        total_possible += t.points
        row = {"test": t.fn.__name__, "points": points, "possible": t.points}
        if points != t.points:
            row["log"] = print_buf.getvalue().split("\n")
        results["tests"].append(row)
        print_buf = None # stop tracing prints
        print("{} of {} points".format(points, t.points))

    print("="*40)
    print("Earned {} of {} points across all tests".format(total_points, total_possible))
    results["score"] = round(100.0 * total_points / total_possible, 1)

    # how long did it take?
    t1 = time.time()
    max_sec = 60
    sec = t1-t0
    if sec > max_sec/2:
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

    print("="*40)
    print("SCORE: %.1f%% (details in results.json)" % results["score"])

########################################
# TESTS
########################################

# see https://en.wikipedia.org/wiki/Web_Server_Gateway_Interface#Example_of_calling_an_application
def app_get(path, expect_str=True, expect_errors=False):
    errors = StringIO()

    environ = {
        "REQUEST_METHOD": "GET",
        "PATH_INFO": path,
        'SERVER_NAME': '0.0.0.0',
        'SERVER_PORT': '3210',
        "SERVER_PROTOCOL": "HTTP/1.1",
        "wsgi.version": (1,0),
        "wsgi.url_scheme": "http",
        "wsgi.input": StringIO(""),
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
            assert status is not None and headers is not None, \
                "start_response() was not called"
            body.write(data)
    finally:
        if hasattr(app_iter, 'close'):
            app_iter.close()

    errors = errors.getvalue()
    if errors and not expect_errors:
        print(errors)

    body = body.getvalue()
    if expect_str:
        body = str(body, "utf-8")
    return status, headers, body

@test(points=10)
def has_pages():
    points = 0
    for page in ["/", "browse.html", "api.html", "donate.html"]:
        status, headers, body = app_get(page)
        if status == "200 OK":
            points += 1
            if body.lower().find("<h1>") >= 0:
                points += 1
            else:
                print("page missing h1 title:", page)
        else:
            print("missing page:", page)

    status, headers, body = app_get("/missing.html", expect_errors=True)
    if status == "404 NOT FOUND":
        points += 2
    else:
        print("404 should be returned for a request to missing.html, but got", status)

    return points

@test(points=10)
def test_browse():
    points = 0
    status, headers, body = app_get("/browse.html")
    dfs = pd.read_html(body)
    if len(dfs) == 1:
        points += 2
    else:
        print("browse.html should have exactly one table, but it had ", len(dfs))
        return 0

    df = dfs[0]
    if len(df) == len(main_df):
        points += 5
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
                    err = "found {} but expected {} at row {} of column {}"
                    err = err.format(actual.iat[i], expected.iat[i], i, col)
                    print(err)
                    eq = False
                    break
            if not eq:
                break

        if eq:
            points += 3
    else:
        print("the browse.html table should have {} rows, not {}".format(len(main_df), len(df)))
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
