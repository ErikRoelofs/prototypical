from tests.basicTest import BasicTest
from reader.number import read_number
from reader.number import read_float

class NumberReaderTest (BasicTest):
    def run(self):
        self.runNumberTests()
        self.runFloatTests()

    def ensureNotAllowed(self, fn, number, message):
        try:
            fn(number)
            assert False, message
        except ValueError:
            return True # this should not be allowed


    def runNumberTests(self):
        assert read_number("12") == 12
        assert read_number("1") == 1
        assert read_number("0") == 0
        assert read_number("99999") == 99999

        self.ensureNotAllowed(read_number, "2.0", "Floats are not supported")
        self.ensureNotAllowed(read_number, "2.5", "Floats are not supported")
        self.ensureNotAllowed(read_number, "abc", "Text is not supported")
        self.ensureNotAllowed(read_number, "", "Blank is not supported")

    def runFloatTests(self):
        assert read_float("1.5") == 1.5
        assert read_float("1.0") == 1
        assert read_float("3") == 3
        self.ensureNotAllowed(read_float, "abc", "Text is not supported")
        self.ensureNotAllowed(read_float, "", "Blank is not supported")
