from sheetParser.complexTypeParser import ComplexTypeParser
from tests.basicTest import BasicTest

class ComplexTypeParserTest (BasicTest):

    def run(self):

        try:
            ComplexTypeParser.validateAllowed("a", 0, 0, {}), "Any char should be allowed in the top left corner"
            ComplexTypeParser.validateAllowed("a", 0, 1, {"b": (0,0,0,0)}), "A new char can follow a different one"
            ComplexTypeParser.validateAllowed("a", 0, 1, {"a": (0,0,0,0)}), "The same char can follow on the next cell"
            ComplexTypeParser.validateAllowed("a", 0, 1, {"a": (0, 0, 0, 0)}), "The same char can follow on the next cell"
            ComplexTypeParser.validateAllowed("a", 1, 0, {"a": (0, 0, 0, 0)}), "The same char can follow on the next line"
        except ValueError as e:
            raise e

        self.ensureNotAllowed("a", 1, 1, {"a": (0, 2, 0, 4)}, "Should not be possible for a char to be more left than its bounding box.")
        self.ensureNotAllowed("a", 2, 0, {"a": (0, 0, 0, 4)}, "Should not be possible for a char to skip a row.")
        self.ensureNotAllowed("e", 1, 1, {"a": (0, 0, 1, 2)}, "Should not be possible for the wrong char to be inside another area.")

    def ensureNotAllowed(self, char, row, col, areas, msg):
        try:
            ComplexTypeParser.validateAllowed(char, row, col, areas)
            assert False, msg
        except ValueError as e:
            True # this should not be allowed
