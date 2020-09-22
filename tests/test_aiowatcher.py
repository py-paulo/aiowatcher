import aiounittest
import os
import sys
from aiowatcher import AIOWatcher


TESTFN = 'testfile.log'
TESTFN2 = 'testfile2.log'
PY3 = sys.version_info[0] == 3


def write_file(data, fp):
    fp.write(data)
    fp.flush()


class TestAIOWatcher(aiounittest.AsyncTestCase):

    lines = []
    filename = []

    async def callback(self, filename, lines):
        self.filename.append(filename)
        for line in lines:
            self.lines.append(line)

    async def test_no_lines(self):
        aiow = AIOWatcher(os.getcwd(), self.callback)
        await aiow.loop(blocking=False)
