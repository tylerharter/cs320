import base64
import importlib
import itertools
import json
import math
import os
import re
import sqlite3
import subprocess
import sys
import time
import traceback
from collections import namedtuple
from datetime import datetime
from io import StringIO

import numpy as np
from matplotlib import pyplot as plt

land = None  # land module

########################################
# TEST FRAMEWORK
########################################

TestFunc = namedtuple("TestFunc", ["fn", "points"])
tests = []

prog_name = "main.py"


# if @test(...) decorator is before a function, add that function to test_fucns
def test(points):
    def add_test(fn):
        tests.append(TestFunc(fn, points))
        return fn

    return add_test


# override print so can also capture output for results.json
print_buf = None
orig_print = print


def print(*args, **kwargs):
    orig_print(*args, **kwargs)
    if print_buf is not None:
        orig_print(*args, **kwargs, file=print_buf)


# both are simple name => val
# expected_json <- expected.json (before tests)
# actual_json -> actual.json (after tests)
#
# TIP: to generate expected.json, run the tests on a good
# implementation, then copy actual.json to expected.json
expected_json = None
actual_json = {"version": 1}


# return string (error) or None
def is_expected2(actual, name, histo_comp=False):
    global expected_json

    actual_json[name] = actual
    if expected_json is None:
        with open("expected.json") as f:
            expected_json = json.load(f)

    expected = expected_json.get(name, None)

    # for hist_comp, we don't care about order of the two list like
    # objects.  We just care that the two histograms are similar.
    if histo_comp:
        if actual is None or expected is None:
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

    elif isinstance(expected, (np.float64, np.float32, float)) and isinstance(actual, (np.float64, np.float32, float)):
        if not math.isclose(float(expected), float(actual)):
            return "{} is not close to {}".format(expected, actual)

    elif type(expected) != type(actual) and expected is not None and actual is not None:
        return "expected a {} but found {} of type {}".format(type(expected), actual, type(actual))

    elif expected != actual:
        return "expected {} but found {}".format(expected, actual)

    return None


# wraps is_expected, just adds name to error messages
def is_expected(actual, name, histo_comp=False):
    err = is_expected2(actual, name, histo_comp)
    if err:
        return f"{err} [BAD {name}]"
    return None


# execute every function with @test decorator; save results to results.json
def run_all_tests(mod_name):
    global land, print_buf
    print("Running tests...")

    land = importlib.import_module(mod_name)

    results = {'score': 0, 'tests': [], 'lint': [], "date": datetime.now().strftime("%m/%d/%Y")}
    total_points = 0
    total_possible = 0

    t0 = time.time()
    for t in tests:
        print_buf = StringIO()  # trace prints
        print("=" * 40)
        print("TEST {} ({} points possible)".format(t.fn.__name__, t.points))
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
        print_buf = None  # stop tracing prints
        print("TEST RESULT: {} of {} points".format(points, t.points))

    print("=" * 40)
    print("Earned {} of {} points across all tests".format(total_points, total_possible))
    results["score"] = round(100.0 * total_points / total_possible, 1)

    # how long did it take?
    t1 = time.time()
    max_sec = 240
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

    # does tester.py version match expected.json version?
    if actual_json["version"] != expected_json["version"]:
        print("#" * 80)
        print("#" * 80)
        print("#")
        if actual_json["version"] > expected_json["version"]:
            print("# WARING! There's a newer version of expected.json, please re-download")
        else:
            print("# WARING! There's a newer version of tester.py, please re-download")
        print("#")
        print("#" * 80)
        print("#" * 80)


########################################
# TESTS
########################################

@test(points=5)
def conn_cleanup():
    points = 0

    c1 = land.open("images")
    err = is_expected(type(c1).__name__, "conn_cleanup:type-name")
    if err:
        print(err)
        return 0

    points += 1

    try:
        c1.db.execute("select * from sqlite_master")
        points += 1
    except sqlite3.ProgrammingError:
        print("1 - db connection isn't open for an open land.Connection")

    c1.close()
    try:
        c1.db.execute("select * from sqlite_master")
        print("c1.close() didn't close underlying db")
    except sqlite3.ProgrammingError:
        points += 1

    if not (hasattr(c1, "__enter__") and hasattr(c1, "__exit__")):
        print("Connection is not a context manager (missing special functions)")
        return points

    with land.open("images") as c2:
        try:
            c2.db.execute("select * from sqlite_master")
            points += 1
        except sqlite3.ProgrammingError:
            print("2 - db connection isn't open for an open land.Connection")

    try:
        c2.db.execute("select * from sqlite_master")
        print("underlying db not closed after context manager exit")
    except sqlite3.ProgrammingError:
        points += 1

    return points


@test(points=5)
def list_images():
    points = 0
    with land.open("images") as c:
        imgs = c.list_images()
        points += 2

        err = is_expected(imgs, "list_images")
        if err:
            print(err)
        else:
            points += 3
    return points


@test(points=5)
def image_year():
    points = 0
    errs = []
    c = land.open("images")
    for i in range(170):
       img = "area%d.npy" % i
       err = is_expected(c.image_year(img), "image_year:%d" % i)
       if err:
          errs.append(err)
    c.close()
    if errs: 
        print(errs[0])
        points = 1
    else:
        points = 5
    return points


@test(points=5)
def image_name():
    points = 0
    errs = []
    c = land.open("images")
    for i in range(170):
        img = "area%d.npy" % i
        err = is_expected(c.image_name(img), "image_name:%d" % i)
        if err:
            errs.append(err)
    c.close()
    if errs:
        print(errs[0])
        points = 1
    else:
        points = 5
    return points


@test(points=5)
def image_load():
    points = 0
    errs = []
    c = land.open("images")
    for i in range(170):
        img = "area%d.npy" % i
        matrix = c.image_load(img)
        shape = [int(x) for x in matrix.shape]
        err = is_expected(shape, "image_load:shape:%d" % i)
        if err:
            errs.append(err)
        else:
            point_sample = [int(x) for x in matrix[::150, ::150].reshape(-1)]
            err = is_expected(point_sample, "image_load:points:%d" % i)
            if err:
                errs.append(err)
    c.close()
    if errs:
        print(errs[0])
        points = 1
    else:
        points = 5
    return points

class WrapAx:
    def __init__(self, ax):
        self.ax = ax
        self.xs = []
        self.ys = []

    def plot(self, *args, **kwargs):
        self.ax.plot(*args, **kwargs)

    def scatter(self, x, y, *args, **kwargs):
        self.xs.extend(x)
        self.ys.extend(y)
        self.ax.scatter(x, y, *args, **kwargs)

    def __getattr__(self, attr):
        return getattr(self.ax, attr)
    
@test(points=5)
def plot_img():
    points = 0
    c = land.open("images")
    
    for i in range(5):
        img = "area%d.npy" % i
        fig, ax = plt.subplots()
        ax = WrapAx(ax)
        c.plot_img(img, ax=ax)
        
        if str(c.image_year(img)) in str(ax.ax.title):
            points += 1
        else:
            print("couldn't find year in title for " + img)
        
        if str(c.image_name(img)) in str(ax.ax.title).lower():
            points += 1
        else:
            print("couldn't find city name in title for " + img)
    
    c.close()
    return points // 2

@test(points=20)
def lat_regression():
    points = 0
    usage_codes_full = [11, 12, 21, 22, 23, 24, 31, 41, 42, 43, 51, 52, 71, 72, 73, 74, 81, 82, 90, 95]
    c = land.open("images")

    # For each usage code
    for usage_code in usage_codes_full:
        fig, ax = plt.subplots()
        ax = WrapAx(ax)
        slope, intercept = c.lat_regression(usage_code, ax=ax)

        # Test slope and intercept
        err = is_expected(actual=slope, name="lat_regression:use_code_slope:%d" % usage_code)
        err = is_expected(actual=intercept, name="lat_regression:use_code_intercept:%d" % usage_code)

        if err is not None:
            print("wrong output for code {}: {}".format(usage_code, err))
        else:
            points += 3

        try:
            check = {
                "all_xs": [round(item, 4) for item in ax.xs],
                "all_ys": [round(item, 4) for item in ax.ys]
            }
        except:
            check = {
                "all_xs": [round(item, 4) for item in list(itertools.chain.from_iterable(ax.xs))],
                "all_ys": [round(item, 4) for item in list(itertools.chain.from_iterable(ax.ys))]
            }

        # Check x's and y's of scatter points
        for key in check:
            err = is_expected(check[key], name="lat_reg_plot:%s:%d" % (key, usage_code), histo_comp=True)
            if err is not None:
                print("distribution of scatter points %s not correct: %s" % (key, err))
            else:
                points += 1

        # Check line and its slope
        if len(ax.lines) == 1:
            slope = round((ax.lines[0].get_ydata()[1] - ax.lines[0].get_ydata()[0]) /
                          (ax.lines[0].get_xdata()[1] - ax.lines[0].get_xdata()[0]), 4)
            err = is_expected(float(slope), name="lat_reg_plot_slope:%s" % (usage_code))
            if err is not None:
                print("incorrect slope of line for code %d: %s" % (usage_code, err))
            else:
                points += 1
        else:
            print("incorrect number of lines (%d) detected for usage_code %d" % (len(ax.lines), usage_code))
        plt.close(fig)

    c.close()
    return points // 6  # 6 points available for each of 20 cases


@test(points=25)
def city_regression():
    calls = [
        {'year': 2050, 'codes': [81, 82]},
        {'year': 7510, 'codes': [11, 12]},
        {'year': 2200, 'codes': [21, 22, 23, 24]},
        {'year': 2525, 'codes': [41, 42, 43]},
        {'year': 2030, 'codes': [51, 52, 71, 72, 73, 74, 81, 82, 90, 95]}
    ]
    
    points = 0
    c = land.open("images")
    
    for params in calls:
        city, prediction = c.city_regression(params['codes'], params['year'])

        err = is_expected(actual=city, name="city_regression:{}:city".format(str(params['year'])))
        if err is not None:
            print("wrong output for year {}: {}".format(str(params['year']), err))
        else:
            points += 3
        
        err = is_expected(actual=prediction, name="city_regression:{}:pred".format(str(params['year'])))
        if err is not None:
            print("wrong output for year {}: {}".format(str(params['year']), err))
        else:
            points += 2

    c.close()
    return points

@test(points=25)
def city_plot():
    points = 0
    cities = ['kenosha', 'racine', 'appleton', 'waukesha', 'janesville']
    c = land.open("images")
    
    for city in cities:
        ax = c.city_plot(city)
        
        # check number of lines
        err = is_expected(actual=len(ax.lines), name="city_plot:{}:numLines".format(city))
        if err is not None:
            print("wrong number of lines for city {}: {}".format(city, err))
        else:
            points += 2
            
        # might have to just check if they're close...
        # people might find the percents differently
        plot_points = [line._y[2] for line in ax.lines] # only check one of the middle points
        err = is_expected(actual=plot_points, name="city_plot:{}:points".format(city), histo_comp=True)
        if err is not None:
            print("wrong points for city {}: {}".format(city, err))
            print("possible precision error")
        else:
            points += 2
            
        if len(ax.legend().texts) != len(ax.lines):
            print('differing number of lines and labels in legend')
        else:
            points += 1
    
    c.close()
    return points

#@test(points=0)
def animate():
    # if you can spell all of these cities w/o help, that's how you know 
    # you're from Wisconsin
    cities = ['madison', 'greenbay', 'eauclaire', 'milwaukee', 'oshkosh']
            #  'kenosha', 'racine', 'appleton', 'waukesha', 'janesville']

    # mostly from p4 tester.py
    vid_mp4 = "extract-vid.mp4"
    points = 0
    c = land.open("images")

    for city in cities:  # for each city, check if it made a video w/ 7+ frames
        if os.path.exists(vid_mp4):
            os.remove(vid_mp4)

        html = c.animate(city)

        m = re.search(r'src\="([^"]+)"', html)
        if m is None:
            print("could not find video src embedded in HTML file")
            continue
        src = m.group(1)
        parts = src.split(",")
        with open(vid_mp4, "wb") as f:
            f.write(base64.b64decode(parts[1]))

        output = subprocess.check_output(["ffprobe", vid_mp4], universal_newlines=True, stderr=subprocess.STDOUT)

        points += 2
        fps = None
        seconds = None
        m = re.search(r"(\d+) fps", output)  # get frames
        if m:
            fps = int(m.group(1))

        m = re.search(r"Duration: ([\d\:\.]*)", output)  # get seconds
        if m:
            seconds = float(m.group(1).split(":")[-1])

        if fps is None and seconds is None:
            print(output)
            print("had trouble finding fps*seconds for {}: {}*{}".format(fps, seconds, city))
        else:
            frames = round(fps * seconds)
            if frames < 7:
                print("expected at least 7 frames for {}".format(city))
            else:
                points += 3

    c.close()
    return points 


########################################
# RUNNER
########################################

def main():
    # import land.py (or other, if specified)
    mod_name = "land"
    if len(sys.argv) > 2:
        print("Usage: python3 test.py [mod_name]")
        sys.exit(1)
    elif len(sys.argv) == 2:
        mod_name = sys.argv[1]

    run_all_tests(mod_name)


if __name__ == "__main__":
    main()
