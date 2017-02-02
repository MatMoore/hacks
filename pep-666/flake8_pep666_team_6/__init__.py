import itertools
import ast

class Linter:
    name = "pep666-team-6"
    version = '0.1'

    def __init__(self, tree, filename, lines=None):
        self.lines = lines
        self.tree = tree

    def line_too_short(self, line):
        return len(line) <= 80

    def line_starts_with_4_spaces(self, line):
        leading_spaces = list(itertools.takewhile(lambda x: x == ' ', line))
        return leading_spaces and len(leading_spaces) % 4 == 0

    def spaces_around_binary_operator(self, line):
        for operator in ['+', '-', '/', '*', '^', '=']:
            for template in [' {}', '{} ']:
                if template.format(operator) in line:
                    return True
        return False

    def blank_line(self, line):
        return len(line) <= 1

    def run(self):
        for line_number, line in enumerate(self.lines):
            if self.line_too_short(line):
                yield (
                    line_number + 1,
                    0,
                    "{0} {1}".format(666, "Line too short"),
                    Linter,
                )

            if self.line_starts_with_4_spaces(line):
                yield (
                    line_number + 1,
                    0,
                    "{0} {1}".format(666, "Line starts with multiply of 4 spaces"),
            if self.blank_line(line):
                yield (
                    line_number + 1,
                    0,
                    "{0} {1}".format(6661, "Save space. Avoid blank lines!"),
                    Linter,
                )
            if self.spaces_around_binary_operator(line):
                yield (
                    line_number + 1,
                    0,
                    "{0} {1}".format(666, "Spaces found around a binary operator"),
                    Linter,
                )

            if self.spaces_around_binary_operator(line):
                yield (
                    line_number + 1,
                    0,
                    "{0} {1}".format(666, "Spaces found around a binary operator"),
                    Linter
                )

        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                yield (
                    node.lineno,
                    0,
                    "{0} {1}".format(666, "Use a lambda instead of def"),
                    Linter,
                )
