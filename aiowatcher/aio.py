import os
import errno
import stat
import asyncio

from aiofile import AIOFile, Reader, LineReader


class AioWatcher(object):
    """Looks for changes in all files of a directory.
    This is useful for watching log file changes in real-time.
    It also supports files rotation.

    Is a library to write concurrent code using the async/await syntax.
    Is often a perfect fit for IO-bound and high-level structured network code.

    >>> import asyncio
    ...
    >>> async def callback(filename, lines):
    ...     print(filename, lines)
    ...
    >>> async def main():
    ...     lw = AioWatcher('var', callback)
    ...     await lw.init()
    ...
    >>> loop = asyncio.get_event_loop()
    >>> loop.run_until_complete(main())
    """

    def __init__(self, folder: str, callback: callable, filename=None, extensions=None, sizehint=1048576):
        """start class instance with some validation, 
        but before using the "init" function it must be called

        Args:
            folder (str): folder containing the files to be monitored
            callback (callable): callback function to handle new entries
            filename (str, optional): name of the only file to be monitored. Defaults to None.
            extensions (list, optional): file extensions to be monitored. Defaults to None.
            sizehint (int, optional): line size that will be read. Defaults to 1048576.
        """
        self.folder = os.path.realpath(folder)
        self.extensions = extensions if isinstance(extensions, list) else ['log']
        self._files_map = {}  # {fid: {'afp': AIOFile, 'offset': int}}
        self._callback = callback
        self._sizehint = sizehint
        self._filename = filename

        assert os.path.isdir(self.folder), self.folder
        assert callable(callback), repr(callback)

    @classmethod
    async def tail(cls, fname, window):
        pass

    async def init(self) -> None:
        """update file status and add to file map
        """
        await self.update_files()

    async def loop(self, interval=5, blocking=True):
        """Start a busy loop checking for file changes every *interval*
        seconds. If *blocking* is False make one loop then return.
        """
        # May be overridden in order to use pyinotify lib and block
        # until the directory being watched is updated.
        # Note that directly calling readlines() as we do is faster
        # than first checking file's last modification times.
        while True:
            await self.update_files()

            for _, dafp in list(self._files_map.items()):
                await self.readlines(dafp)
                
            if not blocking:
                return
            await asyncio.sleep(interval)

    async def update_files(self) -> None:
        """updates, adds or removes mapped files for monitoring
        """
        ls = []
        if self._filename is not None:
            self._stat_file(self._filename, ls)
        else:
            for name in self.listdir():
                self._stat_file(name, ls)

        # check existent files
        for fid, dafp in list(self._files_map.items()):
            try:
                st = os.stat(dafp['afp'].name)
            except EnvironmentError as err:
                # the file no longer exists or may have 
                # been moved to another path
                if err.errno == errno.ENOENT:
                    self.unwatch(dafp, fid)
                else:
                    raise
            else:
                if fid != self.get_file_id(st):
                    # same name but different file (rotation); reload it.
                    self.unwatch(dafp, fid)
                    await self.watch(dafp['afp'].name)

        # add new ones
        for fid, fname in ls:
            if fid not in self._files_map:
                await self.watch(fname)

    async def readlines(self, dafp):
        """Read file lines since last access until EOF is reached and
        invoke callback.
        Updates the *offset* at the end of the file
        """
        reader = Reader(dafp['afp'], offset=dafp['offset'], chunk_size=self._sizehint)
        async for line in reader:
            await self._callback(dafp['afp'].name, line)
        dafp['offset'] = os.path.getsize(dafp['afp'].name)

    async def watch(self, fname):
        try:
            afp = await self.open(fname)
            fid = self.get_file_id(os.stat(fname))
        except EnvironmentError as err:
            if err.errno != errno.ENOENT:
                raise
        else:
            self._files_map[fid] = {'afp': afp, 'offset': os.path.getsize(afp.name)}

    async def unwatch(self, dafp, fid):
        # File no longer exists. If it has been renamed try to read it
        # for the last time in case we're dealing with a rotating log file.
        self.log("un-watching logfile %s" % dafp['afp'].name)
        del self._files_map[fid]

        async with dafp['afp'] as afp:
            # go through the rest of the lines before stop monitoring the file. 
            # does the same as the "readlines" function with the difference 
            # that it does not update the * offset * as in the "readlines" function
            async for line in LineReader(afp, offset=dafp['offset'], chunk_size=self._sizehint):
                await self._callback(dafp['afp'].name, line)

    @classmethod
    async def open(cls, file: str) -> AIOFile:
        """creates a read-only AIOFile instance
        Args:
            file (str): full file path
        Returns:
            AIOFile: open file
        """
        afp = await AIOFile(file, "r")
        return afp

    async def close(self) -> None:
        """closes all open files and clears file map
        """
        for _, dafp in self._files_map.items():
            await dafp['afp'].close()
        self._files_map.clear()

    def log(self, line: str) -> None:
        """log when a file is un/watched
        Args:
            line (str): text
        """
        print(line)

    def _stat_file(self, name: str, ls: list) -> None:
        """get unique file identifier and add a tuple and list passed 
        as an argument with the file ID and the full path respectively

        if the file is not found it will not be added to the list 
        instead of throwing an exception

        Args:
            name (str): filename
            ls (list): list with file names and their respective IDs
        """
        abs_name = os.path.realpath(os.path.join(self.folder, name))
        try:
            st = os.stat(abs_name)
        except EnvironmentError as err:
            if err.errno != errno.ENOENT:
                raise
        else:
            if not stat.S_ISREG(st.st_mode):
                return

            ls.append((self.get_file_id(st), abs_name))

    @staticmethod
    def get_file_id(st) -> str:
        """get the file ID in a different format depending on the platform

        Args:
            st ([type]): result of the "os.stat" call
        Returns:
            str: file ID
        """
        if os.name == 'posix':
            return "%xg%x" % (st.st_dev, st.st_ino)
        else:
            return "%f" % st.st_ctime

    def listdir(self) -> list:
        """list with all files in a directory

        if you have passed a list of extensions in the object instance, 
        a filter will be made

        Returns:
            list: [description]
        """
        ls = os.listdir(self.folder)
        if self.extensions:
            return [x for x in ls if os.path.splitext(x)[1][1:] in self.extensions]
        else:
            return ls

    def __aenter__(self):
        """method for using class in a context"""
        return self

    async def __aexit__(self, *args):
        """method for using class in a context"""
        await self.close()

