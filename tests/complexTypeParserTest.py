from sheetParser.complexTypeParser import ComplexTypeParser

class ComplexTypeParserTest:

    def run(self):

        try:
            ComplexTypeParser.validateAllowed("a", 0, 0, {}), "Any char should be allowed in the top left corner"
            ComplexTypeParser.validateAllowed("a", 0, 1, {"b": (0,0,0,0)}), "A new char can follow a different one"
            ComplexTypeParser.validateAllowed("a", 0, 1, {"a": (0,0,0,0)}), "The same char can follow on the next cell"
            ComplexTypeParser.validateAllowed("a", 0, 1, {"a": (0, 0, 0, 0)}), "The same char can follow on the next cell"
            ComplexTypeParser.validateAllowed("a", 1, 0, {"a": (0, 0, 0, 0)}), "The same char can follow on the next line"
        except ValueError as e:
            raise e

        try:
            ComplexTypeParser.validateAllowed("a", 1, 1, {"a": (0, 2, 0, 4)})
            assert False, "Should not be possible for a char to be more left than its bounding box."
        except ValueError as e:
            True # this should not be allowed

        try:
            ComplexTypeParser.validateAllowed("a", 2, 0, {"a": (0, 0, 0, 4)})
            assert False, "Should not be possible for a char to skip a row."
        except ValueError as e:
            True # this should not be allowed

        try:
            ComplexTypeParser.validateAllowed("e", 1, 1, {"a": (0, 0, 1, 2)})
            assert False, "Should not be possible for the wrong char to be inside another area."
        except ValueError as e:
            True # this should not be allowed