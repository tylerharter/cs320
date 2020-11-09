import sys, json, io, time, traceback, itertools, re, os, math, base64
import traceback, csv, struct, socket, subprocess
from collections import namedtuple
from datetime import datetime, timedelta
from matplotlib import pyplot as plt
from io import StringIO, BytesIO
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from zipfile import ZipFile, ZIP_DEFLATED
from io import TextIOWrapper
from xml.dom import minidom

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
    if print_buf != None:
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

    elif type(expected) != type(actual) and expected != None and actual != None:
        return "expected a {} but found {} of type {}".format(expected, actual, type(actual))

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
def run_all_tests():
    global print_buf
    print("Running tests...")

    results = {'score':0, 'tests': [], 'lint': [], "date":datetime.now().strftime("%m/%d/%Y")}
    total_points = 0
    total_possible = 0

    t0 = time.time()
    for t in tests:
        print_buf = StringIO() # trace prints
        print("="*40)
        print("TEST {} ({} points possible)".format(t.fn.__name__, t.points))
        try:
            points = t.fn()
        except subprocess.CalledProcessError as exc:
            print(exc.returncode, exc.output)
            points = 0
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
        print("TEST RESULT: {} of {} points".format(points, t.points))

    
    # how long did it take?
    t1 = time.time()
    max_sec = 240
    sec = t1-t0
    if sec > 90:
        print("WARNING!  Tests took", sec, "seconds")
        print("Try to keep test under 90 seconds.")
        print("Make sure you have an O(N) implementation for country")
        print("-5 points")
        total_points -= 5
           
    print("="*40)
    print("Earned {} of {} points across all tests".format(total_points, total_possible))
    results["score"] = round(100.0 * total_points / total_possible, 1)

    results["latency"] = sec

    # output results
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    with open("actual.json", "w", encoding="utf-8") as f:
        json.dump(actual_json, f, indent=2)

    print("="*40)
    print("SCORE: %.1f%% (details in results.json)" % results["score"])

    # does tester.py version match expected.json version?
    if actual_json["version"] != expected_json["version"]:
        print("#"*80)
        print("#"*80)
        print("#")
        if actual_json["version"] > expected_json["version"]:
            print("# WARING! There's a newer version of expected.json, please re-download")
        else:
            print("# WARING! There's a newer version of tester.py, please re-download")
        print("#")
        print("#"*80)
        print("#"*80)

########################################
# TESTS
########################################

header = "ip,date,time,zone,cik,accession,extention,code,size,idx,norefer,noagent,find,crawler,browser".split(",")
ip_idx = header.index("ip")
date_idx = header.index("date")
time_idx = header.index("time")
cik_idx = header.index("cik")
accession_idx = header.index("accession")

def gen(row_count=10, sort=False, name=None):
    # name of test that called this
    if name == None:
        name = traceback.extract_stack()[-2].name

    ip_part = 1
    def next_ip_part():
        nonlocal ip_part
        ip_part *= 13
        ip_part %= 256
        return str(ip_part)

    def next_ip():
        ip = ".".join([next_ip_part() for i in range(3)])
        anon = "".join(["abcdefghij"[int(c)] for c in next_ip_part()])
        return ip + "." + anon

    # https://stackoverflow.com/questions/9590965/convert-an-ip-string-to-a-number-and-vice-versa
    def fill_accession(row):
        orig = row[ip_idx][:row[ip_idx].rindex(".")]+".000"
        row[accession_idx] = struct.unpack("!L", socket.inet_aton(orig))[0]

    rows = []
    seconds = 0
    for i in range(row_count):
        row = ["?" for i in range(len(header))]
        row[ip_idx] = next_ip()
        row[date_idx] = "2017-01-01"
        seconds = (seconds * 17) % (24 * 60 * 60)
        row[time_idx] = "%02d:%02d:%02d" % ((seconds//3600) % 24, (seconds//60) % 60, seconds % 60)
        row[cik_idx] = "cik"+str(i)
        fill_accession(row)
        rows.append(row)

    if sort:
        rows.sort(key=lambda row: row[accession_idx])

    zipname = name+".zip"
    with ZipFile(zipname, "w", compression=ZIP_DEFLATED) as zf:
        with zf.open(name+".csv", "w") as raw:
            with TextIOWrapper(raw) as f:
                writer = csv.writer(f, lineterminator='\n')
                writer.writerow(header)
                for row in rows:
                    writer.writerow(row)
    return zipname

def svg_analyze(fname):
    doc = minidom.parse(fname)

    
    try:
        stats = {
            "paths": 0,
            "colors": set(),
            "width": float(doc.getElementsByTagName("svg")[0].getAttribute("width").replace("pt", ""))
        }
    except: # don't think this is needed but just to be safe I guess
        stats = {
            "paths": 0,
            "colors": set(),
            "width": float(doc.getElementsByTagName("svg")[0].getAttribute("width").split(".")[0])
        }

    rgb = [0, 0, 0]
    
    for path in doc.getElementsByTagName('path'):
        style = path.getAttribute('style')
        m = re.match(r"fill:\#(\w+)\;", style)
        if m:
            color = m.group(1).lower()
            if color == "ffffff":
                continue
            stats["colors"].add(color)
            for i in range(3):
                rgb[i] += int(color[i*2:(i+1)*2], 16)
        else:
            continue
        stats["paths"] += 1

    stats["colors"] = len(stats["colors"])
    rgb = "".join([format(int(c/stats["paths"]), "x") for c in rgb])
    stats["avg_color"] = rgb
    return stats

def run(*args):
    args = ["python3", prog_name] + [str(a) for a in args] 
    print("RUN:", " ".join(args))
    subprocess.check_output(
        args, stderr=subprocess.STDOUT,
        universal_newlines=True
    )


def zip_csv_iter(name):
    with ZipFile(name) as zf:
        with zf.open(name.replace(".zip", ".csv")) as f:
            reader = csv.reader(TextIOWrapper(f))
            for row in reader:
                yield row

def check_zip(zname):
    rows = list(zip_csv_iter(zname))
    errors = [is_expected(len(rows)-1, zname+":length")]

    for i, row in enumerate(rows):
        errors.append(is_expected(len(rows), zname+":row-%d:length" % i))

        ip = row[ip_idx]
        cik = row[cik_idx]
        errors.append(is_expected(ip, zname+":row-%d:ip" % i))
        errors.append(is_expected(cik, zname+":row-%d:cik" % i))

    errors = [e for e in errors if e != None]
    if errors:
        return errors[0]
    return None

@test(points=10)
def small_samp():
    points = 0
    zname = gen()
    
    for mod in range(1, 6):
        zout = zname.replace(".zip", "-%d.zip"%mod)
        run("sample", zname, zout, mod)
        err = check_zip(zout)
        if err:
            print(err)
        else:
            points += 2
    return points

@test(points=10)
def big_samp():
    zname = "jan1.zip"
    zout = "jan1-samp.zip"
    run("sample", zname, zout, 1000)
    err = check_zip(zout)
    if err:
        print(err)
        return 0
    return 10

@test(points=10)
def small_country():
    zname = gen(row_count=50)
    zout = zname.replace(".zip", "_output.zip")
    run("country", zname, zout)
    err = check_zip(zout)
    if err:
        print(err)
        return 0
    else:
        return 10

@test(points=20)
def big_country():
    zname = "small.zip" 
    zout = "country_output.zip"
    run("country", zname, zout)
    err = check_zip(zout)
    if err:
        print(err)
        return 0
    return 20

@test(points=25)
def geocontinent():
    zname = "countries.zip"
    svg = "geo.svg"
    if os.path.exists(svg):
        os.remove(svg)
    run("geocontinent", zname, svg, 'Europe')
    stats = svg_analyze(svg)
    if stats["paths"] < 270 or stats["paths"] > 300:
        print("that doesn't look like a world map")
        return 0
    
    # preliminary tests
    points = 25
    if stats["paths"] > 284:
        print("ERROR: please remove Antartica")
        points -= 5

    if stats["colors"] < 3:
        print("ERROR: use more different shades to represent traffic levels")
        points -= 5

    if stats["width"] < 450:
        print("ERROR: make the plot wider")
        points -= 5
      
    avg_colors = set()      
    for continent in ['Europe', 'North America', 'Asia', 'South America', 'Australia', 'Africa']:
        svg = "geo{}.svg".format(continent.split()[0])
        if os.path.exists(svg):
            os.remove(svg)
        run("geocontinent", zname, svg, continent)
        stats = svg_analyze(svg)
        avg_colors.add(stats["avg_color"])

    if len(avg_colors) < 5:
        print("colors don't seem to change much from hour to hour")
        points -= 10

    return points

@test(points=15)
def geohour():
    zname = "countries.zip"
    avg_colors = set()
    points = 15
    
    for hour in range(0, 24, 4):
        svg = "geo-%d.svg" % hour
        if os.path.exists(svg):
            os.remove(svg)
        run("geohour", zname, svg, hour)
        stats = svg_analyze(svg)
        if stats["paths"] < 270 or stats["paths"] > 300:
            print("%s doesn't look like a world map" % svg)
            return 0
        avg_colors.add(stats["avg_color"])
        
        # check json file
        with open('top_5_h{}.json'.format(hour), 'r') as f:
            top_5 = json.load(f)
        err = is_expected(sorted(top_5.values()), 'geohour_json_{}'.format(hour))
        if err is not None:
            points -= 1
            print('incorrect top 5 for hour {}'.format(hour))

    if len(avg_colors) < 3:
        print("colors don't seem to change much from hour to hour")
        return 0

    return points

@test(points=10)
def video():
    zname = "countries.zip"
    vid_html = "test-vid.html"
    vid_mp4 = "extract-vid.mp4"
    for p in (vid_html, vid_mp4):
        if os.path.exists(p):
            os.remove(p)

    run("video", zname, vid_html)

    # try to extract video
    with open(vid_html) as f:
        html = f.read()
    m = re.search(r'src\="([^"]+)"', html)
    if m == None:
        print("could not find video src embedded in HTML file")
        return 0
    src = m.group(1)
    parts = src.split(",")
    with open(vid_mp4, "wb") as f:
        f.write(base64.b64decode(parts[1]))

    print("Using ffprobe to check video (install with 'sudo apt install ffmpeg' if you don't have it)")
    output = subprocess.check_output(["ffprobe", vid_mp4], universal_newlines=True, stderr=subprocess.STDOUT)

    points = 5
    fps = None
    seconds = None
    m = re.search(r"(\d+) fps", output)
    if m:
        fps = int(m.group(1))
    m = re.search(r"Duration: ([\d\:\.]*)", output)
    if m:
        seconds = float(m.group(1).split(":")[-1])
    if fps == None and seconds == None:
        print(output)
        print("had trouble finding fps*seconds: {}*{}".format(fps, seconds))
    else:
        frames = round(fps*seconds)
        if frames < 22 or frames > 26:
            print("expected 24 frames")
        else:
            points += 5

    return points

########################################
# RUNNER
########################################

def main():
    global prog_name
    
    # import main.py (or other, if specified)
    prog_name = "main.py"
    if len(sys.argv) > 2:
        print("Usage: python3 test.py [prog_name]")
        sys.exit(1)
    elif len(sys.argv) == 2:
        prog_name = sys.argv[1]
        if not prog_name.endswith(".py"):
            prog_name += ".py"

    run_all_tests()

if __name__ == "__main__":
    main()
