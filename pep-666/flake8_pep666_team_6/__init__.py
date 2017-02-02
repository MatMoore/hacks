class Linter:
    name = "pep666-team-6"
    version = '0.1'

    def __init__(self, tree, filename, lines=None):
        self.lines = lines
        self.tree = tree

    @classmethod
    def add_options(cls, parser):
        # List of application import names. They go last.
        pass

    @classmethod
    def parse_options(cls, options):
        optdict = {}

        cls.options = optdict

    def line_too_short(self, line):
        return len(line) <= 80

    def run(self):
        for line_number, line in enumerate(self.lines):
            if self.line_too_short(line):
                yield (
                    line_number + 1,
                    0,
                    "{0} {1}".format(666, "Line too short"),
                    Linter,
                )
