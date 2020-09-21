import asyncio
import aiounittest
import os
import sys
import unittest
import atexit
import aiofile
from aiowatcher import AIOWatcher

TESTFN = '$testfile.log'
TESTFN2 = '$testfile2.log'
PY3 = sys.version_info[0] == 3

if PY3:
    def b(s):
        return s.encode("latin-1")
else:
    def b(s):
        return s

class TestAIOWatcher(aiounittest.AsyncTestCase):

    def __init__(self, methodName='runTest', loop=None):
        self.loop = loop or asyncio.get_event_loop()
        self._function_cache = {}
        super(TestAIOWatcher, self).__init__(methodName=methodName)

    async def setUp(self):
        async def callback(filename, lines):
            self.filename.append(filename)
            for line in lines:
                self.lines.append(line)

        self.filename = []
        self.lines = []
        self.file = open(TESTFN, 'w')
        self.watcher = AIOWatcher(os.getcwd(), callback)

    async def tearDown(self):
        await self.watcher.close()
        self.remove_test_files()

    def write_file(self, data):
        self.file.write(data)
        self.file.flush()

    @staticmethod
    @atexit.register
    def remove_test_files():
        for x in [TESTFN, TESTFN2]:
            try:
                os.remove(x)
            except EnvironmentError:
                pass

    async def test_no_lines(self):
        await self.watcher.loop(blocking=False)

    async def test_one_line(self):
        self.write_file('foo')
        await self.watcher.loop(blocking=False)
        self.assertEqual(self.lines, [b"foo"])
        self.assertEqual(self.filename, [os.path.abspath(TESTFN)])

    async def test_two_lines(self):
        self.write_file('foo\n')
        self.write_file('bar\n')
        await self.watcher.loop(blocking=False)
        self.assertEqual(self.lines, [b"foo\n", b"bar\n"])
        self.assertEqual(self.filename, [os.path.abspath(TESTFN)])

    async def test_new_file(self):
        with open(TESTFN2, "w") as f:
            f.write("foo")
        await self.watcher.loop(blocking=False)
        self.assertEqual(self.lines, [b"foo"])
        self.assertEqual(self.filename, [os.path.abspath(TESTFN2)])

    async def test_file_removed(self):
        self.write_file("foo")
        try:
            os.remove(TESTFN)
        except EnvironmentError:  # necessary on Windows
            pass
        await self.watcher.loop(blocking=False)
        self.assertEqual(self.lines, [b"foo"])

    async def test_ctx_manager(self):
        async with self.watcher:
            pass
