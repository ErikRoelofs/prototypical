from tests.basicTest import BasicTest
from reader.color import ColorReader

class ColorReaderTest (BasicTest):
    def run(self):
        assert ColorReader.read_color("red") == (1,0,0)
        assert ColorReader.read_color("#00ff00") == (0,1,0)
        assert ColorReader.read_color("#000099") == (0, 0, 0.6)
        assert ColorReader.read_color("#999900") == (0.6,0.6,0)

        self.ensureNotAllowed("123", "123 is not a color")
        self.ensureNotAllowed("text", "text is not a color")
        self.ensureNotAllowed("]", "empty string is not a color")

    def ensureNotAllowed(self, value, msg):
        try:
            ColorReader.read_color(value)
            assert False, msg
        except ValueError:
            1