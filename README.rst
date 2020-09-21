AIOWatcher
==========

.. image:: https://img.shields.io/github/languages/code-size/py-paulo/aiowatcher   :alt: GitHub code size in bytes

.. image:: https://img.shields.io/github/license/py-paulo/aiowatcher   :alt: GitHub

Library to "watch" files in a directory and call a callback function (file name, lines) every time one of the files being monitored is recorded, in real time.

Practically speaking, this can be compared to `tail -F *.log` UNIX command, but instead of having lines printed to stdout a python function gets called.

Similarly to tail, it takes care of "watching" new files which are created after initialization and "unwatching" those ones which are removed in the meantime. This means you'll be able to "follow" and support also rotating log files.

Code examples
-------------

All code examples requires python 3.6+.

Basic Usage
+++++++++++

.. code-block:: python

    import asyncio
    from aiowatcher import AIOWatcher

    async def callback(filename, line):
        print(line)

    async def main():
        lw = AIOWatcher('var', callback, extensions=['txt'])
        await lw.init()
        await lw.loop()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())    


Non blocking
++++++++++++

.. code-block:: python

    import asyncio
    from aiowatcher import AIOWatcher

    async def callback(filename, line):
        print(line)

    async def main():
        lw = AIOWatcher('var', callback, extensions=['txt'])
        while True:
            await lw.loop(blocking=False)
            await asyncio.sleep(0.1)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


