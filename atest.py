import time
import asyncio
from queue import Queue
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import aiohttp

from pprint import pprint


class AsyncTestA:
    def __init__(self):
        self.__executor = ThreadPoolExecutor(max_workers=2)
        self.__async_loop_A = asyncio.new_event_loop()
        self.__executor.submit(self.print_manager, self.__async_loop_A)
        self.session = None

    def print_manager(self, loop):
        asyncio.set_event_loop(loop=loop)
        loop.run_forever()

    async def call_print(self, count: int):
        print(
            f"Count: {count}, @{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}"
        )
        await asyncio.sleep(0.1)

    async def depth_poller(self):
        self.session = aiohttp.ClientSession()
        async with self.session.get(
                "https://api.kucoin.com/v1/open/orders",
                params={
                    "symbol": "USE-ETH",
                    "limit": 100
                }) as response:
            msg = await response.json()
            pprint(msg)

    def starter(self):

        asyncio.run_coroutine_threadsafe(self.depth_poller(),
                                         self.__async_loop_A)

        while True:
            time.sleep(1)

        # loop = asyncio.get_event_loop()
        # loop.run_until_complete(self.depth_poller())


class AsyncTestB:
    def __init__(self):
        self.__loop = asyncio.get_event_loop()
        self.__task = asyncio.gather(self.call_print())
        self.__loop.run_until_complete(self.__task)

    async def call_print(self):
        count = 0
        while count < 100:
            count += 1
            msg = f"Count: {count}, @{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}"
            asyncio.run_coroutine_threadsafe(self.print_x(msg), self.__loop)
            await asyncio.sleep(0.01)

    async def print_x(self, msg):
        print(msg)
        await asyncio.sleep(0.1)


class AsyncTestC:
    def __init__(self):
        self.__loop = asyncio.get_event_loop()
        self._i = 0
        while self._i < 1000:
            self.__task = [
                self.call_print(self._i),
                self.call_print(self._i + 1)
            ]
            self._i += 2
            self.__loop.run_until_complete(asyncio.wait(self.__task))

    async def call_print(self, count: int):
        print(
            f"Count: {count}, @{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}"
        )
        await asyncio.sleep(0.033)


if __name__ == '__main__':
    # Double Thread for Async
    x = AsyncTestA()
    x.starter()

    # Single Thread for Async
    # x = AsyncTestB()

    # Single Thread for Async
    # x = AsyncTestC()
