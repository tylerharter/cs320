#!/usr/bin/python

import json
import os
import sys
import re, ast, math
from collections import namedtuple, OrderedDict, defaultdict
from bs4 import BeautifulSoup
from datetime import datetime
import nbconvert
import nbformat
import numpy as np
from numpy import array

#try:
 #   from lint import lint
#except ImportError:
 #   err_msg = """Please download lint.py and place it in this directory for 
  #  the tests to run correctly. If you haven't yet looked at the linting module, 
   # it is designed to help you improve your code so take a look at: 
    #https://github.com/tylerharter/cs320/tree/master/linter"""
    #raise FileNotFoundError(err_msg)

ALLOWED_LINT_ERRS = {
  "W0703": "broad-except",
  "R1716": "chained-comparison",
  "E0601": "used-before-assignment",
  "W0105": "pointless-string-statement",
  "E1135": "unsupported-membership-test",
  "R1711": "useless-return",
  "W0143": "comparison-with-callable",
  # Removed due to pytorch error
  # "E1102": "not-callable",
  "W0107": "unnecessary-pass",
  "W0301": "unnecessary-semicolon",
  "W0404": "reimported",
  "W0101": "unreachable",
  "R1714": "consider-using-in",
  "W0311": "bad-indentation",
  "E0102": "function-redefined",
  "E0602": "undefined-variable",
  "W0104": "pointless-statement",
  "W0622": "redefined-builtin",
  "W0702": "bare-except",
  "R1703": "simplifiable-if-statement",
  "W0631": "undefined-loop-variable",
}

PASS = 'PASS'
FAIL_STDERR = 'Program produced an error - please scroll up for more details.'
FAIL_JSON = 'Expected program to print in json format. Make sure the only print statement is a print(json.dumps...)!'
EPSILON = 0.0001


TEXT_FORMAT = "text"
PNG_FORMAT = "png"
HTML_FORMAT = "html"
NUMPY_FORMAT = "numpy"
VIDEO_FORMAT = "mp4"
Question = namedtuple("Question", ["number", "weight", "format"])

questions = [
    Question(number=1, weight=1, format=NUMPY_FORMAT),
    Question(number=2, weight=1, format=NUMPY_FORMAT),
    Question(number=3, weight=1, format=TEXT_FORMAT),
    Question(number=4, weight=1, format=TEXT_FORMAT),
    Question(number=5, weight=1, format=TEXT_FORMAT),
    Question(number=6, weight=1, format=HTML_FORMAT),
    Question(number=7, weight=1, format=HTML_FORMAT),
    Question(number=8, weight=1, format=PNG_FORMAT),
    Question(number=9, weight=1, format=TEXT_FORMAT),
    Question(number=10, weight=1, format=NUMPY_FORMAT),
    Question(number=11, weight=1, format=HTML_FORMAT),
    Question(number=12, weight=1, format=TEXT_FORMAT),
    Question(number=13, weight=1, format=TEXT_FORMAT),
    Question(number=14, weight=1, format=NUMPY_FORMAT),
    Question(number=15, weight=1, format=NUMPY_FORMAT),
    Question(number=16, weight=1, format=NUMPY_FORMAT),
    Question(number=17, weight=1, format=NUMPY_FORMAT),
    Question(number=18, weight=1, format=NUMPY_FORMAT),
    
]
question_nums = set([q.number for q in questions])

expected_json = {
    "1": ((50803, 50), (50963, 50)),
    "2": (4.401295199102416, 4.390695210250574, 2.984025665505041, 2.9862059667206435),
    "3": {'train': {'NO': 27360, '>30': 17770, '<30': 5673}, 'test': {'NO': 27504, '>30': 17775, '<30': 5684}},
    "4": {'race': 2.2104993799578763,
          'weight': 96.80924354860933,
          'payer_code': 39.25949254965258,
          'medical_specialty': 49.180166525598885,
          'diag_1': 0.023620652323681674,
          'diag_2': 0.3444678463870244,
          'diag_3': 1.3955868747908586},
    "5": ['admission_source_id','admission_type_id','discharge_disposition_id',
          'encounter_id','num_lab_procedures','num_medications','num_procedures','number_diagnoses',
          'number_emergency','number_inpatient','number_outpatient','patient_nbr','time_in_hospital'],
    "9": {'font12plus': True,
          'transparency': True,
          'x-label': 'visits',
          'y-label': 'days in hospital',
          'spines': False,
          'x-mean': 2.2887866256900424,
          'y-mean': 2.983996296763971,
          'x-std': 1.206208294785741,
          'y-std': 4.401295199102416,
          'slope': 0.03951032525517387,
          'intercept': 4.353637517049943},
    "10": (0.0009184071670116367, 0.001087944356748527),
    "_11": {'font12plus': True,
           'transparency': True,
           'x-label': 'days in hospital',
           'y-label': 'lab procedures done',
           'spines': False,
           'x-mean': 2.983996296763971,
           'y-mean': 19.769919407825235,
           'x-std': 4.401295199102416,
           'y-std': 43.155915989213234,
           'slope': 2.119487878508591,
           'intercept': 33.8274241649776},
    "_12": (0.10234075960861977, 0.1004406985134011),
    "12": "stay = 0.32*AfricanAmerican + -0.29*Asian + 0.04*Caucasian + -0.14*Hispanic + -0.10*Other + 3.42*Female + 3.28*Male + 0.02*age + -0.45",
    "13": (0.014362012823362136, 0.012415699517403067),
    "14": (0.8883333661397949, 0.8884681043109707),
    "15": (0.8883333661397949, 0.8884681043109707),
    "16": [[45279, 0], [5684, 0]],
    "17": [[32725, 12554], [3105, 2579]],
    "18": [[43630, 1649], [5363, 321]],
}

def parse_df_html_table(html, question=None):
    soup = BeautifulSoup(html, 'html.parser')

    if question == None:
        tables = soup.find_all('table')
        assert(len(tables) == 1)
        table = tables[0]
        # log actual output (useful for manually creating expected.html...)
        with open("out.txt", "a") as f:
            f.write(table.prettify())
    else:
        # find a table that looks like this:
        # <table data-question="6"> ...
        table = soup.find('table', {"data-question": str(question)})

    rows = []
    for tr in table.find_all('tr'):
        rows.append([])
        for cell in tr.find_all(['td', 'th']):
            rows[-1].append(cell.get_text().strip())

    cells = {}
    for r in range(1, len(rows)):
        for c in range(1, len(rows[0])):
            rname = rows[r][0]
            cname = rows[0][c]
            cells[(rname.lower(),cname.lower())] = rows[r][c]
    return cells


# find a comment something like this: #q10
def extract_question_num(cell):
    for line in cell.get('source', []):
        line = line.strip().replace(' ', '').lower()
        m = re.match(r'\#q(\d+)', line)
        if m:
            return int(m.group(1))
    return None


# rerun notebook and return parsed JSON
def rerun_notebook(orig_notebook):
    new_notebook = 'cs-320-test.ipynb'

    # re-execute it from the beginning
    with open(orig_notebook, encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=nbformat.NO_CONVERT)
    ep = nbconvert.preprocessors.ExecutePreprocessor(timeout=120, kernel_name='python3')
    try:
        out = ep.preprocess(nb, {'metadata': {'path': os.getcwd()}})
    except nbconvert.preprocessors.CellExecutionError:
        out = None
        msg = 'Error executing the notebook "%s".\n\n' % orig_notebook
        msg += 'See notebook "%s" for the traceback.' % new_notebook
        print(msg)
        raise
    finally:
        with open(new_notebook, mode='w', encoding='utf-8') as f:
            nbformat.write(nb, f)

    # Note: Here we are saving and reloading, this isn't needed but can help student's debug

    # parse notebook
    with open(new_notebook,encoding='utf-8') as f:
        nb = json.load(f)
    return nb


def normalize_json(orig):
    try:
        return json.dumps(json.loads(orig.strip("'")), indent=2, sort_keys=True)
    except:
        return 'not JSON'


def get_cell_output(cell, mime):
    outputs = cell.get('outputs', [])
    actual_lines = None
    for out in outputs:
        lines = out.get('data', {}).get(mime, [])
        if lines:
            actual_lines = lines
            break
    return actual_lines


def check_cell_text(qnum, cell):
    if len(cell.get('outputs', [])) == 0:
        return 'no outputs in an Out[N] cell'

    actual_lines = get_cell_output(cell, "text/plain")
    if actual_lines == None:
        return 'no Out[N] output found for cell (note: printing the output does not work)'

    actual = ''.join(actual_lines)
    try:
        actual = ast.literal_eval(actual)
    except Exception as e:
        print("COULD NOT PARSE THIS CELL:")
        print(actual)
        raise e
    expected = expected_json[str(qnum)]

    expected_mismatch = False

    if type(expected) != type(actual):
        return "expected an answer of type %s but found one of type %s" % (type(expected), type(actual))
    elif type(expected) == float:
        if not math.isclose(actual, expected, rel_tol=1e-02, abs_tol=1e-02):
            expected_mismatch = True
    elif type(expected) == list:
        try:
            extra = set(actual) - set(expected)
            missing = set(expected) - set(actual)
            if missing:
                return "missing %d entries list, such as: %s" % (len(missing), repr(list(missing)[0]))
            elif extra:
                return "found %d unexpected entries, such as: %s" % (len(extra), repr(list(extra)[0]))
            elif len(actual) != len(expected):
                return "expected %d entries in the list but found %d" % (len(expected), len(actual))
            else:
                for i,(a,e) in enumerate(zip(actual, expected)):
                    if a != e:
                        return "found %s at position %d but expected %s" % (str(a), i, str(e))
        except TypeError:
            if len(actual) != len(expected):
                return "expected %d entries in the list but found %d" % (len(expected), len(actual))
            for i,(a,e) in enumerate(zip(actual, expected)):
                if a != e:
                    return "found %s at position %d but expected %s" % (str(a), i, str(e))            # this happens when the list contains dicts.  Just do a simple comparison
    elif type(expected) == tuple:
        if len(expected) != len(actual):
            expected_mismatch = True
        try:
            for idx in range(len(expected)):
                if not math.isclose(actual[idx], expected[idx], rel_tol=1e-02, abs_tol=1e-02):
                    expected_mismatch = True
        except Exception as e:
            print(e)
            expected_mismatch = True

    elif type(expected) == dict:
        ek = set(expected.keys())
        ak = set(actual.keys())
        if ak-ek:
            return "unexpected key: {}".format(list(ak-ek)[0])
        elif ek-ak:
            return "missing key: {}".format(list(ek-ak)[0])
        for k in expected:
            if type(expected[k]) == float:
                if not math.isclose(expected[k], actual[k]):
                    return f"found {repr(actual[k])} for key {repr(k)} but found expected {repr(expected[k])}"
            elif expected[k] != actual[k]:
                return f"found {repr(actual[k])} for key {repr(k)} but found expected {repr(expected[k])}"

    else:
        if expected != actual:
            expected_mismatch = True

    if expected_mismatch:
        return "found {} in cell {} but expected {}".format(actual, qnum, expected)

    return PASS


def diff_df_cells(actual_cells, expected_cells):
    for location, expected in expected_cells.items():
        location_name = "column {} at index {}".format(location[1], location[0])
        actual = actual_cells.get(location, None)
        if actual == None:
            return 'value missing for ' + location_name
        try:
            actual_float = float(actual)
            expected_float = float(expected)
            if math.isnan(actual_float) and math.isnan(expected_float):
                return PASS
            if not math.isclose(actual_float, expected_float, rel_tol=1e-02, abs_tol=1e-02):
                print(type(actual_float), actual_float)
                return "found {} in {} but it was not close to expected {}".format(actual, location_name, expected)
        except Exception as e:
            if actual != expected:
                return "found '{}' in {} but expected '{}'".format(actual, location_name, expected)
    return PASS


def check_cell_html(qnum, cell):
    actual_lines = get_cell_output(cell, "text/html")
    if actual_lines == None:
        return 'no Out[N] output found for cell (note: printing the output does not work)'

    try:
        actual_cells = parse_df_html_table(''.join(actual_lines))
    except Exception as e:
        print("ERROR!  Could not find table in notebook")
        raise e

    try:
        with open('expected.html') as f:
            expected_cells = parse_df_html_table(f.read(), qnum)
    except Exception as e:
        print("ERROR!  Could not find table in expected.html")
        raise e

    return diff_df_cells(actual_cells, expected_cells)


def check_cell_png(qnum, cell):
    for output in cell.get('outputs', []):
        if 'image/png' in output.get('data', {}):
            return PASS
    return 'no plot found'


def check_cell_numpy(qnum, cell):
    if len(cell.get('outputs', [])) == 0:
        return 'no outputs in an Out[N] cell'

    actual_lines = get_cell_output(cell, "text/plain")
    if actual_lines == None:
        return 'no Out[N] output found for cell (note: printing the output does not work)'

    actual = ''.join(actual_lines)
    try:
        actual = eval(actual)
    except Exception as e:
        print("COULD NOT PARSE THIS CELL:")
        print(actual)
        raise e
    expected = expected_json[str(qnum)]

    actual = np.array(actual)
    expected = np.array(expected)
    if not np.allclose(actual, expected):
        actual = re.sub(r"\s+", " ", repr(actual))
        expected = re.sub(r"\s+", " ", repr(expected))
        return f"np.allclose({actual}, {expected}), comparing actual to expected, failed"
    return PASS

def check_cell_video(qnum, cell):
    actual_lines = get_cell_output(cell, "text/html")
    if actual_lines == None:
        return 'no Out[N] output found for cell (note: printing the output does not work)'
    actual = ''.join(actual_lines)
    if actual.find("<video") < 0:
        return "no <video> tag found in output"
    return PASS

def check_cell(question, cell):
    print('Checking question %d' % question.number)
    if question.format == TEXT_FORMAT:
        return check_cell_text(question.number, cell)
    elif question.format == PNG_FORMAT:
        return check_cell_png(question.number, cell)
    elif question.format == HTML_FORMAT:
        return check_cell_html(question.number,cell)
    elif question.format == NUMPY_FORMAT:
        return check_cell_numpy(question.number,cell)
    elif question.format == VIDEO_FORMAT:
        return check_cell_video(question.number, cell)
    raise Exception("invalid question type")


def grade_answers(cells):
    results = {'score':0, 'tests': [], 'lint': [], "date":datetime.now().strftime("%m/%d/%Y")}

    for question in questions:
        cell = cells.get(question.number, None)
        status = "not found"

        if question.number in cells:
            # does it match the expected output?
            status = check_cell(question, cells[question.number])

        row = {"test": question.number, "result": status, "weight": question.weight}
        results['tests'].append(row)

    return results


def main():
    # rerun everything
    orig_notebook = 'main.ipynb'
    if len(sys.argv) > 2:
        print("Usage: test.py main.ipynb")
        return
    elif len(sys.argv) == 2:
        orig_notebook = sys.argv[1]

    # make sure directories are properly setup

    nb = rerun_notebook(orig_notebook)

    # extract cells that have answers
    answer_cells = {}
    for cell in nb['cells']:
        q = extract_question_num(cell)
        if q == None:
            continue
        if not q in question_nums:
            print('no question %d' % q)
            continue
        answer_cells[q] = cell

    # do grading on extracted answers and produce results.json
    results = grade_answers(answer_cells)
    passing = sum(t['weight'] for t in results['tests'] if t['result'] == PASS)
    total = sum(t['weight'] for t in results['tests'])

   # lint_msgs = lint(orig_notebook, verbose=1, show=False)
   # lint_msgs = filter(lambda msg: msg.msg_id in ALLOWED_LINT_ERRS, lint_msgs)
   # lint_msgs = list(lint_msgs)
    #results["lint"] = [str(l) for l in lint_msgs]

    functionality_score = 100.0 * passing / total
    #linting_score = min(10.0, len(lint_msgs))
    results['score'] = max(functionality_score, 0.0) 
    # subtract linting_score from functionality_score to add linter back in

    print("\nSummary:")
    for test in results["tests"]:
        print("  Question %d: %s" % (test["test"], test["result"]))

    #if len(lint_msgs) > 0:
     #   msg_types = defaultdict(list)
      #  for msg in lint_msgs:
       #     msg_types[msg.category].append(msg)
       # print("\nLinting Summary:")
        #for msg_type, msgs in msg_types.items():
         #   print('  ' + msg_type.title() + ' Messages:')
          #  for msg in msgs:
           #     print('    ' + str(msg))

    print('\nTOTAL SCORE: %.2f%%' % results['score'])
    with open('result.json', 'w') as f:
        f.write(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
