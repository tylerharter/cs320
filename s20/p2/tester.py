import importlib, sys, json, io, time, traceback, itertools
from datetime import datetime, timedelta
from collections import namedtuple
from matplotlib import pyplot as plt
bus = None # bus module

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
        return "expected a {} but found {} of type {}".format(expected, actual, type(actual))

    elif expected != actual:
            return "expected {} but found {}".format(expected, actual)

    return None

# execute every function with @test decorator; save results to results.json
def run_all_tests(mod_name="bus"):
    global bus, print_buf
    print("Running tests...")

    bus = importlib.import_module(mod_name)

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
        json.dump(actual_json, f, indent=2)

    print("="*40)
    print("SCORE: %.1f%% (details in results.json)" % results["score"])

########################################
# TESTS
########################################

day_cache = {}
def get_day(date):
    if not date in day_cache:
        day_cache[date] = bus.BusDay(date)
    return day_cache[date]

@test(points=8)
def has_classes():
    points = 0
    for name in ["BusDay", "Location", "Stop", "Trip"]:
        if hasattr(bus, name) and type(getattr(bus, name)) == type:
            points += 2
        else:
            print("no class named "+name)
    return points

@test(points=20)
def service_ids():
    points = 0
    for i, day in enumerate([datetime(2020, 2, 21), datetime(2020, 2, 22)]):
        bd = get_day(day)
        service_ids = sorted(bd.service_ids)

        err = is_expected(actual=service_ids, name="service_ids:%d"%i)
        if err != None:
            print("unexpected service_ids for {}: {}".format(day, err))
            continue

        points += 10
    return points

@test(points=8)
def get_trips():
    points = 0

    for i, day in enumerate([datetime(2020, 2, 21), datetime(2020, 2, 22)]):
        bd = get_day(day)
        trips = bd.get_trips()

        err = is_expected(actual=len(trips), name="get_trips:len:%d"%i)
        if err != None:
            print("unexpected len results for get_trips() results on {}: {}".format(day, err))
        else:
            points += 2

        first5 = [repr(t) for t in trips[:5]]
        err = is_expected(actual=first5, name="get_trips:repr:%d"%i)
        if err != None:
            print("unexpected repr results in first 5 get_trips results on {}: {}".format(day, err))
        else:
            points += 2

    return points

@test(points=10)
def get_trips_by_route():
    points = 0
    bd = get_day(datetime(2020, 2, 21))
    for route in range(100):
        trips = bd.get_trips(route)
        err = is_expected(actual=len(trips), name="get_trips_by_route:len:%d"%route)
        if err != None:
            print("wrong number of trips for route {}: {}".format(route, err))
        else:
            points += 1
    return points // 10

@test(points=8)
def get_stops():
    points = 0

    for i, day in enumerate([datetime(2020, 2, 21), datetime(2020, 2, 22)]):
        bd = get_day(day)
        stops = bd.get_stops()

        err = is_expected(actual=len(stops), name="get_stops:len:%d"%i)
        if err != None:
            print("unexpected len results for get_stops() results on {}: {}".format(day, err))
        else:
            points += 2

        first5 = [repr(t) for t in stops[:5]]
        err = is_expected(actual=first5, name="get_stops:repr:%d"%i)
        if err != None:
            print("unexpected repr results in first 5 get_stops() results on {}: {}".format(day, err))
        else:
            points += 2

    return points


@test(points=10)
def get_stops_rect():
    points = 0
    for day in [datetime(2020, 2, 21), datetime(2020, 2, 22)]:
        dayname = day.strftime("%A").lower()
        bd = get_day(day)
        for i in range(5):
            for j in range(5):
                x1 = i-2
                y1 = j-2
                for k in range(1,5):
                    x2 = x1 + k/4
                    y2 = y1 + k/4
                    stops = bd.get_stops_rect((x1, x2), (y1, y2))
                    name = "{}: len(get_stops_rect(({}, {}), ({}, {})))"
                    name = name.format(dayname, x1, x2, y1, y2)
                    err = is_expected(len(stops), name=name)
                    if err != None:
                        print("%s incorrect: %s" % (name, err))
                    else:
                        points += 0.05
    return int(points)

@test(points=10)
def get_stops_circ():
    points = 0
    for day in [datetime(2020, 2, 21), datetime(2020, 2, 22)]:
        dayname = day.strftime("%A").lower()
        bd = get_day(day)
        for i in range(5):
            for j in range(5):
                x = i-2
                y = j-2
                for r in range(1,5):
                    radius = r/4
                    stops = bd.get_stops_circ((x, y), radius)
                    name = "{}: len(get_stops_circ(({}, {}), {}))"
                    name = name.format(dayname, x, y, radius)
                    err = is_expected(len(stops), name=name)
                    if err != None:
                        print("%s incorrect: %s" % (name, err))
                    else:
                        points += 0.05
    return int(points)

class WrapAx:
    def __init__(self, ax):
        self.ax = ax
        # key: color: list of vals
        self.x = dict()
        self.y = dict()
        self.vlines = []
        self.hlines = []

    def plot(self, *args, **kwargs):
        # Example call: ax.plot((x, x), (y1, y2), 'y', lw=3, zorder=-10)
        if len(args) >= 2 and isinstance(args[0], tuple) and isinstance(args[1], tuple):
            if args[0][0] == args[0][1]:
                # x values are the same, so it is vertical
                self.vlines.append(args[0][0])
            elif args[1][0] == args[1][1]:
                # y values are the same, so it is horizontal
                self.hlines.append(args[1][0])

    def scatter(self, x, y, *args, **kwargs):
        color = kwargs["c"][0]
        if not color in self.x:
            self.x[color] = []
            self.y[color] = []
        self.x[color].extend(x)
        self.y[color].extend(y)
        self.ax.scatter(x, y, *args, **kwargs)

    def __getattr__(self, attr):
        return getattr(self.ax, attr)

@test(points=20)
def scatter_stops():
    points = 0
    for i, day in enumerate([datetime(2020, 2, 21), datetime(2020, 2, 22)]):
        bd = get_day(day)

        fig, ax = plt.subplots(figsize=(10, 10))
        ax = WrapAx(ax)
        bd.scatter_stops(ax)

        check = {
            "all-x": list(itertools.chain.from_iterable(ax.x.values())),
            "all-y": list(itertools.chain.from_iterable(ax.y.values())),
            "red-x": ax.x.get("red", []),
            "red-y": ax.y.get("red", []),
            "gray-x": ax.y.get("0.7", []),
            "gray-y": ax.y.get("0.7", []),
        }
        for key in check:
            err = is_expected(check[key], name="scatter_stops:%s:%d"%(key, i), histo_comp=True)
            if err != None:
                print("distribution of scatter points %s not correct: %s" % (key, err))
            else:
                if key.startswith("all-"):
                    points += 3
                else:
                    points += 1

    return points

@test(points=6)
def draw_tree():
    points = 0
    for i, day in enumerate([datetime(2020, 2, 21), datetime(2020, 2, 22)]):
        bd = get_day(day)
        dayname = day.strftime("%A").lower()

        fig, ax = plt.subplots(figsize=(10, 10))
        ax = WrapAx(ax)
        bd.draw_tree(ax)

        if len(ax.hlines + ax.vlines) > 0:
            points += 1
        else:
            print("no lines detected; did you plot like this?")
            print("ax.plot((x, x), (y1, y2), ...)")
            

        err = is_expected(ax.hlines, name="%s:draw_tree:hlines"%dayname, histo_comp=True)
        if err != None:
            print("horizontal lines not correctly placed: %s" % err)
        else:
            points += 1

        err = is_expected(ax.vlines, name="%s:draw_tree:vlines"%dayname, histo_comp=True)
        if err != None:
            print("vertical lines not correctly placed: %s" % err)
        else:
            points += 1

    return points

########################################
# RUNNER
########################################

def main():
    # import bus.py (or other, if specified)
    mod_name = "bus"
    if len(sys.argv) > 2:
        print("Usage: python3 test.py [mod_name]")
        sys.exit(1)
    elif len(sys.argv) == 2:
        mod_name = sys.argv[1]

    run_all_tests(mod_name)

if __name__ == "__main__":
    main()
