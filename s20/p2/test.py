import importlib, sys, json, io, time, traceback
from datetime import datetime, timedelta
from collections import namedtuple
bus = None # bus module

########################################
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

def is_expected(actual, name):
    global expected_json

    actual_json[name] = actual
    if expected_json == None:
        with open("expected.json") as f:
            expected_json = json.load(f)

    expected = expected_json.get(name, None)

    if type(expected) != type(actual):
        return "expected a {} but found {} of type {}".format(expected, actual, type(actual))

    # TODO: if it's a float, allow some tolerance

    if expected != actual:
        return "expected {} but found {}".format(expected, actual)

    return None

# execute every function with @test decorator; save results to results.json
def run_all_tests():
    global print_buf
    print("Running tests...")

    results = {'score':0, 'tests': [], 'lint': [], "date":datetime.now().strftime("%m/%d/%Y")}
    total_points = 0
    total_possible = 0

    for t in tests:
        print_buf = io.StringIO() # trace prints
        try:
            points = t.fn()
        except Exception as e:
            print(traceback.format_exc())
            points = 0
        assert points <= t.points
        total_points += points
        total_possible += t.points
        row = {"test": t.fn.__name__, "points": points, "possible": t.points}
        if points != t.points:
            row["log"] = print_buf.getvalue().split("\n")
        results["tests"].append(row)
        print_buf = None # stop tracing prints

    results["score"] = round(100.0 * total_points / total_possible, 1)

    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    with open("actual.json", "w", encoding="utf-8") as f:
        json.dump(actual_json, f, indent=2)

    print("="*40)
    print("SCORE: %.1f%% (details in results.json)" % results["score"])

########################################
# TESTS
########################################

@test(5)
def has_classes():
    count = 0
    for name in ["BusDay", "Location", "Stop", "StopTime", "Trip"]:
        if hasattr(bus, name) and type(getattr(bus, name)) == type:
            count += 1
        else:
            print("no class named "+name)
    return count

@test(14)
def service_ids():
    count = 0
    day = datetime(2020, 2, 12)
    for i in range(14):
        day += timedelta(days=1)
        bd = bus.BusDay(day)
        service_ids = sorted(bd.service_ids)

        err = is_expected(actual=service_ids, name="service_ids:%d"%i)
        if err != None:
            print("unexpected service_ids for {}: {}".format(day, err))
            continue

        count += 1
    return count

########################################
# RUNNER
########################################

def main():
    global bus

    # import bus.py (or other, if specified)
    mod_name = "bus"
    if len(sys.argv) > 2:
        print("Usage: python3 test.py [mod_name]")
        sys.exit(1)
    elif len(sys.argv) == 2:
        mod_name = sys.argv[1]
    bus = importlib.import_module(mod_name)

    # run tests to produce results.json
    t0 = time.time()
    run_all_tests()
    t1 = time.time()

    max_sec = 60
    sec = t1-t0
    if sec > max_sec/2:
        print("WARNING!  Tests took", sec, "seconds")
        print("Maximum is ", sec, "seconds")
        print("We recommend keeping runtime under half the maximum as a buffer.")
        print("Variability may cause it to run slower for us than you.")


if __name__ == "__main__":
    main()
