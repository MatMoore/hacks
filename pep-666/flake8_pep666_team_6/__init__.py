import itertools


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
                    Linter,
                )
