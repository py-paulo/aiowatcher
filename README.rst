AIOWatcher
==========

.. image:: https://i.pinimg.com/originals/1b/2a/2a/1b2a2a3a94cae52f318e1893303a0834.png
   :height: 126px
   :width: 256px
   :alt: aiowatcher logo

|

.. image:: https://img.shields.io/github/repo-size/py-paulo/aiowatcher 
    :target: https://img.shields.io/github/repo-size/py-paulo/aiowatcher
    :alt: GitHub repo size

.. image:: https://img.shields.io/pypi/v/AIOWatcher
    :target: https://img.shields.io/pypi/v/aiowatcher
    :alt: PyPI

.. image:: https://img.shields.io/pypi/wheel/aiowatcher
    :target: https://img.shields.io/pypi/wheel/aiowatcher
    :alt: PyPI - Wheel

.. image:: https://img.shields.io/github/license/py-paulo/aiowatcher   
    :target: https://img.shields.io/github/license/py-paulo/aiowatcher
    :alt: GitHub

.. image:: https://img.shields.io/github/last-commit/py-paulo/aiowatcher
    :target: https://img.shields.io/github/last-commit/py-paulo/aiowatcher
    :alt: GitHub last commit

Library to "watch" files in a directory and call a
callback function `(filename, lines)` every time one of the monitored files is recorded, in real time.

In practical terms, this can be compared to UNIX's `tail -F * .log` command,
but instead of having lines printed in stdout, a Python function is called.

Like tail, it is in charge of "watching" new files that are
created after startup and "unlock" those that are removed in the meantime.
This means that you will be able to "follow" and support rotating log files as well.

Key Features
============

- Uses Asyncio for asynchronous reading and monitoring.
- The implementation chooses automatically depending on the compatibility of the system.
- Monitoring of several files in the same directory or just one.
- Asynchronous callback function.

Getting started
---------------

All code samples require Python 3.6+.

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


License
=======

``aiowatcher`` is offered under the Apache 2 license.


Source code
===========

The latest version of the developer is available on a GitHub repository:
https://github.com/py-paulo/aiowatcher.git
