import asyncio
from aiowatch import AIOWatch


async def callback(filename, line):
    print(line)


async def main():
    lw = AIOWatch('var', callback, extensions=['txt'])

    while True:
        await lw.loop(blocking=False)
        await asyncio.sleep(0.1)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
