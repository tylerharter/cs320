import importlib, sys, json, io, time, traceback, itertools, os
from datetime import datetime, timedelta
from collections import namedtuple
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

# hitting lower accuracy corresponds to grade of 0%
# hitting upper accuracy corresponds to grade of 100%
lower = 55
upper = 80
max_sec = 60
module_name = "main"
test_set = "test1"

if len(sys.argv) > 3:
    print("Usage: python3 test.py [mod_name] [test_set]")
    sys.exit(1)
if len(sys.argv) > 1:
    module_name = sys.argv[1]
if len(sys.argv) > 2:
    test_set = sys.argv[2]

student_module = importlib.import_module(module_name)

def main():
    print(f"We'll use this to grade you:\n    python3 tester.py main test2\n")
    print("test2_users.csv and test2_log.csv are secret, so you can use this to estimate your accuracy:\n    python3 tester.py main test1\n")

    print("Grading:")
    print(f"    Max Seconds: {max_sec}")
    print(f"    Accuracy <{lower}: grade=0%")
    print(f"    Accuracy >{upper}: grade=100%")
    print()

    t0 = time.time()
    print("Fitting+Predicting...")

    # step 1: fit
    model = student_module.UserPredictor()
    train_users = pd.read_csv(os.path.join("data", "train_users.csv"))
    train_logs = pd.read_csv(os.path.join("data", "train_logs.csv"))
    train_y = pd.read_csv(os.path.join("data", "train_y.csv"))
    model.fit(train_users, train_logs, train_y)

    # step 2: predict
    test_users = pd.read_csv(os.path.join("data", "{}_users.csv".format(test_set)))
    test_logs = pd.read_csv(os.path.join("data", "{}_logs.csv".format(test_set)))
    y_pred = model.predict(test_users, test_logs)

    # step 3: grading based on accuracy
    y = pd.read_csv(os.path.join("data", "{}_y.csv".format(test_set)))
    accuracy = (y["y"] == y_pred).sum() / len(y) * 100
    grade = round((np.clip(accuracy, lower, upper) - lower) / (upper - lower) * 100, 1)

    t1 = time.time()
    sec = t1-t0
    assert sec < max_sec
    warn_sec = 0.75 * max_sec
    if sec > warn_sec:
        print("="*40)
        print("WARNING!  Tests took", sec, "seconds")
        print("Maximum is ", max_sec, "seconds")
        print(f"We recommend keeping runtime under {warn_sec} seconds to be safe.")
        print("Variability may cause it to run slower for us than you.")
        print("="*40)

    # output results
    results = {"score":grade,
               "accuracy": accuracy,
               "date":datetime.now().strftime("%m/%d/%Y"),
               "latency": sec}
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print("Result:\n" + json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
