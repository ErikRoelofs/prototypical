from tests.basicTest import BasicTest
from reader.dimensions import read_dimensions

class DimensionsReaderTest (BasicTest):
    def run(self):
        assert read_dimensions("200x300") == (200,300)
        assert read_dimensions("1x1") == (1,1)
        assert read_dimensions("1500x1200") == (1500,1200)

        self.ensureNotAllowed("0x100", "Zero should not be allowed")
        self.ensureNotAllowed("-100x100", "Negatives should not be allowed")
        self.ensureNotAllowed("100x-100", "Negatives should not be allowed")
        self.ensureNotAllowed("100", "An x should be required")
        self.ensureNotAllowed("100n50", "An x should be required")
        self.ensureNotAllowed("text", "Both sides should be numbers.")
        self.ensureNotAllowed("100x", "Both sides should exist.")
        self.ensureNotAllowed("x100", "Both sides should exist.")

    def ensureNotAllowed(self, dimensions, message):
        try:
            read_dimensions(dimensions)
            assert False, message
        except ValueError:
            return True # this should not be allowed
