class Linter:
    name = "pep666-team-6"
    version = '0.1'

    def __init__(self, tree, filename, lines=None):
        self.lines = lines
        self.tree = tree
        print(lines)

    @classmethod
    def add_options(cls, parser):
        # List of application import names. They go last.
        pass

    @classmethod
    def parse_options(cls, options):
        optdict = {}

        cls.options = optdict

    def run(self):
        yield (
            1,
            0,
            "{0} {1}".format(666, "This isn't real code"),
            Linter,
        )
