import importlib, sys, json, io, time, traceback, itertools
from datetime import datetime, timedelta
from collections import namedtuple
from matplotlib import pyplot as plt
import pandas as pd
tree = None # tree module

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

# both are simple name => val
# expected_json <- expected.json (before tests)
# actual_json -> actual.json (after tests)
#
# TIP: to generate expected.json, run the tests on a good
# implementation, then copy actual.json to expected.json
expected_json = None
actual_json = {}
EXPECTED_VERSION = 2

def is_expected(actual, name, histo_comp=False):
    global expected_json

    actual_json[name] = actual
    if expected_json == None:
        with open("expected.json") as f:
            expected_json = json.load(f)
            version = expected_json.get("version", 1)
            if version != EXPECTED_VERSION:
                expected_json = None
                raise Exception("this tester.py needs version %d of expected.json, but found version %d" % (EXPECTED_VERSION, version))

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
        if diff > 0.05:
            return "average error between actual and expected was %.2f (>0.05)" % diff

    elif type(expected) != type(actual):
        return "expected a {} but found {} of type {}".format(repr(expected), repr(actual), type(actual))

    elif expected != actual:
            return "expected {} but found {}".format(repr(expected), repr(actual))

    return None

# execute every function with @test decorator; save results to results.json
def run_all_tests(mod_name="tree"):
    global tree, print_buf
    print("Running tests...")
    
    tree = importlib.import_module(mod_name)

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
    if sec > max_sec/2:
        print("WARNING!  Tests took", sec, "seconds")
        print("Maximum is ", max_sec, "seconds")
        print("We recommend keeping runtime under half the maximum as a buffer.")
        print("Variability may cause it to run slower for us than you.")

    results["latency"] = sec

    # output results
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    with open("actual.json", "w", encoding="utf-8") as f:
        actual_json["version"] = EXPECTED_VERSION
        json.dump(actual_json, f, indent=2)

    print("="*40)
    print("SCORE: %.1f%% (details in results.json)" % results["score"])

########################################
# TESTS
########################################

# GROUP

@test(points=5)
def has_classes1():
    points = 0
    for name in ["ZippedCSVReader", "Bank", "Loan", "SimplePredictor", "DTree"]:
        if hasattr(tree, name) and type(getattr(tree, name)) == type:
            points += 1
        else:
            print("no class named " + name)
    return points

@test(points=10)
def testReader():
    points = 0
    reader = tree.ZippedCSVReader('mini.zip')

    err = is_expected(actual=reader.paths, name="testReader:paths")
    if err != None:
        print("unexpected results for paths: {}".format(err))
    else:
        points += 2

    rows = reader.csv_iter()
    err = is_expected(actual=len(list(rows)), name="testReader:csv_iter")
    if err != None:
        print("unexpected results for csv_iter(): {}".format(err))
    else:
        points += 4

    rows = reader.csv_iter()
    err = is_expected(actual=len(list(rows)), name="testReader:csv_iter_wi")
    if err != None:
        print("unexpected results for csv_iter('wi.csv'): {}".format(err))
    else:
        points += 4

    return points

@test(points=3)
def testBankNames():
    reader = tree.ZippedCSVReader('mini.zip')
    err = is_expected(actual=len(list(tree.get_bank_names(reader))), name="testBankNames")
    if err != None:
        print("unexpected results for Bank.get_banks: {}".format(err))
        return 0
    else:
        return 3
            
@test(points=6)
def testBank():
    points = 0
    names = ['NCUA', 'OCC']
    reader = tree.ZippedCSVReader('mini.zip')

    for name in names:
        b = tree.Bank(name, reader)
        err = is_expected(actual=len(list(b.loan_iter())), name="testBank:bank-init-%s"%name)
        if err != None:
            print("unexpected results for creating bank: {}".format(err))
        else:
            points += 3

    return points

def iter_counter(it):
    count = 0
    for _ in it:
        count += 1
    return count

@test(points=10)
def testLoan():
    points = 0
    loan = tree.Loan(40, "Home improvement", "Asian", 120, "approve")
    err = is_expected(actual=loan.__repr__(), name="testLoan:__repr__")
    if err != None:
        print("unexpected results for Loan.__repr__: {}".format(err))
    else:
        points += 2
    for key in ["decision", "income", "Asian", "White", "Home improvement", "Refinance", "amount", "purpose"]:
        err = is_expected(actual=loan[key], name="testLoan:%s"%key)
        if err != None:
            print("unexpected results for Loan['{}']: {}".format(key, err))
        else:
            points += 1
    return points

@test(points=4)
def testSimplePredictor():
    reader = tree.ZippedCSVReader('mini.zip')
    b = tree.Bank(None, reader)
    sp = tree.SimplePredictor()

    mistakes = 0
    for i, row in enumerate(b.loan_iter()):
        y_ = sp.predict(row)
        err = is_expected(actual=y_, name="testSP:predict:%d"%i)
        if err != None:
            print("unexpected results for SimplePredictor.predict: {}".format(err))
            mistakes += 1

    return 4 if mistakes == 0 else 0

@test(points=27)
def testDTree():
    points = 0

    reader = tree.ZippedCSVReader('loans.zip')
    b = tree.Bank(None, reader)
    li = b.loan_iter()
    loans = [next(li) for i in range(100)]

    for path in ['simple.txt', 'good.txt', 'bad.txt']:
        tree_reader = tree.ZippedCSVReader('trees.zip')
        dtree = tree.DTree()
        dtree.readTree(tree_reader, path)

        # test predict
        mistakes = 0
        for i, loan in enumerate(loans):
            y = dtree.predict(loan)
            err = is_expected(actual=y, name="testDTree:predict:%s:%d"%(path,i))
            if err != None:
                mistakes += 1
                print("unexpected results for DTree.predict(): {}".format(err))
        if mistakes == 0:
            points += 7

        # test getApproved
        err = is_expected(actual=dtree.getApproved(), name="testDTree:getApproved:%s"%path)
        if err != None:
            print("unexpected results for DTree.getApproved(): {}".format(err))
        else:
            points += 1

        # test getDisapproved
        err = is_expected(actual=dtree.getDisapproved(), name="testDTree:getDisapproved:%s"%path)
        if err != None:
            print("unexpected results for DTree.getDisapproved(): {}".format(err))
        else:
            points += 1
        
    return points

@test(points=10)
def testLoanFilter():
    points = 0
    reader = tree.ZippedCSVReader('loans.zip')
    
    list_of_things = [('NCUA', 75, 85), ('OCC', 150, 200)]
    for tup in list_of_things:
        b = tree.Bank(tup[0], reader)
        points += 1

        err = is_expected(actual=iter_counter(b.loan_iter()), name="testLoan:loan_iter():%s"%tup[0])
        if err != None:
            print("unexpected results for Loan.get_loans(): {}".format(err))
        else:
            points += 2

        err = is_expected(actual=iter_counter(b.loan_filter(tup[1], tup[2], 'Home purchase')), name="testLoan:loan_filter():%s"%tup[0])
        if err != None:
            print("unexpected results for Loan.specific_loan(): {}".format(err))
        else:
            points += 2

    return points

# INDIVIDUAL

@test(points=9)
def testRF():
    points = 0

    # grab first 100 loans
    reader = tree.ZippedCSVReader('loans.zip')
    b = tree.Bank(None, reader)
    li = b.loan_iter()
    loans = [next(li) for i in range(100)]

    # build 7 trees
    tree_reader = tree.ZippedCSVReader('trees.zip')
    trees = []
    for i in range(1, 8):
        dtree = tree.DTree()
        dtree.readTree(tree_reader, f"tree{i}.txt")
        trees.append(tree)

    # test with varying odd numbers of voters
    for voters in [3,5,7]:
        rf = tree.RandomForest(trees[:voters])
        mistakes = 0
        for i, loan in enumerate(loans):
            y = dtree.predict(loan)
            err = is_expected(actual=y, name=f"testRF:predict:{voters}-trees:{i}")
            if err != None:
                print("unexpected results for random forest predict(): {}".format(err))
        if mistakes == 0:
            points += 3

    return points

@test(points=10)
def testBias():
    points = 0

    reader = tree.ZippedCSVReader('mini.zip')
    b = tree.Bank(None, reader)
    li = b.loan_iter()

    for path in ['good.txt', 'bad.txt']:
        tree_reader = tree.ZippedCSVReader('trees.zip')
        dtree = tree.DTree()
        dtree.readTree(tree_reader, path)

        bias_count = tree.bias_test(b, dtree, "Black or African American")
        err = is_expected(actual=bias_count, name=f"bias_test:{path}")
        if err != None:
            print(f"unexpected results for bias_test on {path}: {err}")
        else:
            points += 5
    return points

@test(points=6)
def testBiasLargeFile():
    points = 0

    reader = tree.ZippedCSVReader('loans.zip')
    b = tree.Bank(None, reader)
    li = b.loan_iter()

    path = "bad.txt"
    tree_reader = tree.ZippedCSVReader('trees.zip')
    dtree = tree.DTree()
    dtree.readTree(tree_reader, path)

    bias_count = tree.bias_test(b, dtree, "Asian")
    err = is_expected(actual=bias_count, name=f"bias_test-largezip:{path}")
    if err != None:
        print(f"unexpected results for bias_test on {path}: {err}")
    else:
        points += 6

    return points

########################################
# RUNNER
########################################

def main():
    # import tree.py (or other, if specified)
    mod_name = "tree"
    if len(sys.argv) > 2:
        print("Usage: python3 test.py [mod_name]")
        sys.exit(1)
    elif len(sys.argv) == 2:
        mod_name = sys.argv[1]

    run_all_tests(mod_name)

if __name__ == "__main__":
    main()
