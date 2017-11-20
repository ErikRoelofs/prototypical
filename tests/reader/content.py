from tests.basicTest import BasicTest
from reader.content import read_content


class ContentReaderTest (BasicTest):
    def run(self):
        assert read_content("5xitem") == [(5, "item"),]
        assert read_content("5xitem;2xother_item") == [(5, "item"),(2, "other_item")]
        assert read_content("item") == [(1, "item"),]
        assert read_content("something;otherthing") == [(1, "something"),(1,"otherthing")]

        assert read_content("itemxitem") == [(1, "itemxitem"),]



    def ensureNotAllowed(self, content, message):
        try:
            read_content(content)
            assert False, message
        except ValueError:
            pass
