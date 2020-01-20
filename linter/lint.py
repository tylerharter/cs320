import re
import os
import argparse
from collections import defaultdict

import nbformat
import numpy as np
from pylint import epylint
import astroid


class LintMessage:
    """A simple data container for each linting message"""
    def __init__(self, path, line, category, msg_id, symbol, obj, msg,
                 cell=None, data=None):
        # Assumes line number and cell number are zero indexed
        self.path, self.line, self.category = path, int(line), category
        self.msg_id, self.symbol, self.obj, self.msg = msg_id, symbol, obj, msg
        self.cell, self.data = cell, data
        self.enhance_msg()

    def enhance_msg(self):
        map = {
            "W0702": "Too broad exception clause. You should try catching "
                     "specific exceptions",
        }
        self.msg = map.get(self.msg_id, self.msg)

    @classmethod
    def from_stdout(cls, stdout, source=None):
        # From the standard out, create one record per linter message
        pattern = r'(\S+):(\d*): (\w*) \((\w*), ([\w-]*), (.*)\) (.*)'
        objects = [cls(*l) for l in re.findall(pattern, stdout)]
        for obj in objects:
            obj.line -= 1
            if source:
                obj.data = source[obj.line]
        return objects

    def __str__(self):
        # Note: cell, line are zero indexed internally but starts at 1
        if self.cell is not None:
            return f'cell: {self.cell+1}, line: {self.line+1} - {self.msg}'
        return f'line: {self.line+1} - {self.msg}'

    def full_str(self, indent=0):
        p = f'{" "*indent}{self.msg_id}, {self.symbol}, ' + self.__str__()
        p += '\n' + " "*indent + 'on line: ' + self.data.strip() + '\n'
        return p


class ScriptLinter:
    def __init__(self, path, verbose=False):
        self.path, self.verbose = path, verbose

    def lint_script(self):
        """Call pylint and create LintMessages for each msg"""
        with open(self.path, 'r', encoding='utf-8') as f:
            source = f.read().splitlines()
        cmd = self.path + ' --persistent=no --score=no'
        pylint_stdout, pylint_stderr = epylint.py_run(cmd, return_std=True)
        stdout = pylint_stdout.getvalue()
        stderr = pylint_stderr.getvalue()
        if stderr:
            print(stderr)
        return LintMessage.from_stdout(stdout, source=source)

    def filter_messages(self, msgs):
        """Filter messages based on verbosity"""
        if self.verbose < 2:
            # Filter out PEP8/Convention formatting stuff if not verbose
            msgs = filter(lambda msg: msg.category != 'convention', msgs)
            # Filter out warnings that aren't severe like redefined-outer-name
            msgs = filter(lambda msg: msg.msg_id != 'W0621', msgs)
        if self.verbose < 1:
            # Filter out warnings if not verbose enough
            msgs = filter(lambda msg: msg.category != 'warning', msgs)
        return list(msgs)

    def run(self):
        msgs = self.lint_script()
        msgs = self.filter_messages(msgs)
        return msgs


class NotebookLinter(ScriptLinter):
    def __init__(self, path, cleanup=True, verbose=False):
        super().__init__(path, verbose=verbose)
        self.cell_lines = []
        self.cleanup = cleanup
        if not path.endswith('.ipynb'):
            raise ValueError('File needs to be a IPython Notebook (.ipynb)')

    def lint_notebook(self):
        """Lint the generated script and map the massages to their
        corresponding cell/line number in the notebook"""
        cell_start_line, _ = self.notebook_mapping()
        lint_msgs = self.lint_script()
        if self.cleanup:
            os.remove(self.path)
        valid_lint_msgs = []
        for lint_msg in lint_msgs:
            try:
                line_offset = int(lint_msg.line) - cell_start_line
                line_offset[line_offset < 0] = line_offset.max()
                cell_num = np.argmin(line_offset)
                cell_line = line_offset[cell_num]
                lint_msg.cell = cell_num
                lint_msg.line = cell_line
                valid_lint_msgs.append(lint_msg)
            except ValueError:
                pass
        return valid_lint_msgs

    def notebook_mapping(self):
        """Map script lines to notebook cell/line number"""
        self.path = self.notebook2script()
        cell_end_lines = np.cumsum(self.cell_lines)
        return cell_end_lines-self.cell_lines, cell_end_lines-1

    def notebook2script(self, script_path=None):
        """Read in notebook, convert to NotebookNode object then
        traverse nodes and join their code together to get the source"""
        if not script_path:
            script_path = self.path.replace('.ipynb', '.py')
        if os.path.isfile(script_path):
            raise IOError(f'File {script_path} exists already, please delete or rename')
        with open(self.path, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=nbformat.NO_CONVERT)
        self.cells = [cell['source'] for cell in nb['cells']
                      if cell['cell_type'] == 'code' and cell['source']]
        source = self.comment_jupyter_magics('\n'.join(self.cells))
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(source)
        self.cell_lines = [len(cell.split('\n')) for cell in self.cells]
        self.cell_lines = np.array(self.cell_lines)
        return script_path

    def comment_jupyter_magics(self, source):
        """Commments out jupyter magics"""
        #TODO: make this more robust, a multiline string can break this.
        cleaned_source = []
        for line in source.splitlines():
            if self.line_is_jupyter_magic(line):
                cleaned_source.append('# ' + line)
            else:
                cleaned_source.append(line)
        return '\n'.join(cleaned_source)

    @staticmethod
    def remove_comments(source):
        return astroid.parse(source).as_string().strip()

    def is_not_jupyter_magic(self, msg):
        is_magic = self.line_is_jupyter_magic(msg.data)
        is_error = msg.msg_id == "E0001"
        return not (is_magic and is_error)

    @staticmethod
    def line_is_jupyter_magic(line):
        return line.startswith('%') or line.startswith('!')

    def last_line_of_code(self, msg):
        #TODO: Tests more, it doesnt work all the time
        cell_str = self.cells[msg.cell]
        cell_str = self.remove_comments(cell_str)
        line_str = self.remove_comments(msg.data)
        return cell_str.endswith(line_str)

    def filter_messages(self, msgs):
        """Filter messages that might have been created due to
        converting the notebook to a script"""
        msgs = super().filter_messages(msgs)
        # Remove expression-not-assigned and pointless-statement warnings
        # If they are the last line of a cell (used to display)
        msgs = filter(lambda msg: msg.msg_id not in ('W0106', 'W0104'), msgs)
        # Remove errors caused by jupyter magics like %matplotlib inline
        msgs = filter(self.is_not_jupyter_magic, msgs)
        return list(msgs)

    def run(self):
        msgs = self.lint_notebook()
        msgs = self.filter_messages(msgs)
        return msgs


def lint(path, *args, show=True, debug=False, **kwargs):
    if path.endswith('.ipynb'):
        linter = NotebookLinter(path, *args, **kwargs)
    else:
        linter = ScriptLinter(path, *args, **kwargs)
    msgs = linter.run()
    if show:
        if not msgs:
            print('No linting messages to show!')
        msg_types = defaultdict(list)
        for msg in msgs:
            msg_types[msg.category].append(msg)
        for msg_type, msgs in msg_types.items():
            print(f'{msg_type.title()} Messages:')
            for msg in msgs:
                print(msg.full_str(indent=2) if debug else '  ' + str(msg))
            print()
        return None
    return msgs


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Linter for CS320')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='Extra information about the linting message')
    parser.add_argument('path', type=str, help='path of file to lint (.ipynb or .py)')
    parser.add_argument('-v', '--verbose', action='count', default=0,
                        help='by default don\'t show warnings nor convention'
                             ' messages, enable with -v and -vv respectively')

    grader_args = parser.parse_args()
    lint(**vars(grader_args))
