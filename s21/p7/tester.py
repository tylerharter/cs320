import importlib, sys, json, io, time, traceback, itertools, os
from datetime import datetime, timedelta
from collections import namedtuple
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

upred = None # main module

test_set = 'test1'
lower = 60
upper = 80

########################################
# TEST FRAMEWORK
########################################

TestFunc = namedtuple("TestFunc", ["fn", "points"])
tests = []

# if @test(...) decorator is before a function, add that function to test_funcs
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


# execute every function with @test decorator; save results to results.json
def run_all_tests(mod_name="main"):
    global upred, print_buf
    print("Running tests...")
    
    upred = importlib.import_module(mod_name)

    results = {'score':0, 'tests': [], 'lint': [], "date":datetime.now().strftime("%m/%d/%Y")}
    total_points = 0
    total_possible = 0

    t0 = time.time()
    for t in tests:
        print_buf = io.StringIO() # trace prints
        print("="*40)
        print("TEST {} ({})".format(t.fn.__name__, t.points))
        try:
            points = t.fn()
        except Exception as e:
            print(traceback.format_exc())
            points = 0
        if points > t.points:
            raise Exception("got {} points on {} but expected at most {}".format(points, t.fn.__name__, t.points))
        print(points, "POINTS")
        total_points += points
        total_possible += t.points
        row = {"test": t.fn.__name__, "points": points, "possible": t.points}
        if points != t.points:
            row["log"] = print_buf.getvalue().split("\n")
        results["tests"].append(row)
        print_buf = None # stop tracing prints

    print("Earned {} of {} points".format(total_points, total_possible))
    results["score"] = round(100.0 * total_points / total_possible, 1)

    # how long did it take?
    t1 = time.time()
    max_sec = 60
    sec = t1-t0
    if sec > 30:
        print("WARNING!  Tests took", sec, "seconds")
        print("Maximum is ", max_sec, "seconds")
        print("We recommend keeping runtime 20 seconds.")
        print("Variability may cause it to run slower for us than you.")

    results["latency"] = sec

    # output results
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    
    print("="*40)
    print("SCORE: %.1f%% (details in results.json)" % results["score"])


########################################
# TESTS
########################################

@test(points=100)
def testUserPredictor():
    # read in csvs
    
    train_users = pd.read_csv(os.path.join('data', "train_users.csv"))
    train_logs = pd.read_csv(os.path.join('data', "train_logs.csv"))
    train_y = pd.read_csv(os.path.join('data', "train_y.csv"))
    
    test_users = pd.read_csv(os.path.join('data', "{}_users.csv".format(test_set)))
    test_logs = pd.read_csv(os.path.join('data', "{}_logs.csv".format(test_set)))
    y = pd.read_csv(os.path.join('data', '{}_y.csv'.format(test_set)))
    
    # make object
    up = upred.UserPredictor()
    up.fit(train_users, train_logs, train_y)
    
    y_pred = up.predict(test_users, test_logs)
    
    # # assumes they are in the same order 
    accuracy = (y['y'] == y_pred).sum()
    
    percent = (np.clip(accuracy, lower, upper) - lower) / (upper - lower) * 100
    
    print("ACCURACY: {}%".format(percent))
    points = int((2 * percent) - 70)
    
    return points if points <= 100 else 100


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