import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor
import time
from pprint import pprint
import json

from util import Util
from depthdata import DepthData
from diff_dict import DiffDict

'''写到redis,增量比对，文件落库'''


class depth:

    def __init__(self):
        self.SYMBOL = {"ETH-BTC": "ETH-BTC"}
        self.__rest_depth_url = "https://api.kucoin.com/v1/open/orders"
        self.session = None

        self.last_data = None

    def run_forever(self):
        self.__loop = asyncio.new_event_loop()
        self.__executor = ThreadPoolExecutor(max_workers=2)
        self.__executor.submit(self.asyncio_initiator, self.__loop)
        asyncio.run_coroutine_threadsafe(self.depth_poller(symbol="ETH-BTC"), self.__loop)
        while True:
            time.sleep(3)

    def asyncio_initiator(self, loop):
        asyncio.set_event_loop(loop=loop)
        loop.run_forever()

    async def depth_poller(self, symbol):
        self.session = aiohttp.ClientSession()

        while True:
            async with self.session.get(url=self.__rest_depth_url, params={"symbol": symbol, "limit": 100},
                                        verify_ssl=False, proxy="http://127.0.0.1:1087") as response:
                json_data = await response.json()

                data = DepthData(symbol, json_data)

                diff = DepthData.get_diff(data, self.last_data)

                self.last_data = data

                Util.write_json_file(diff, Util.get_file_name("depth"))

                # pprint(self.data)

                # break

                await asyncio.sleep(3)  # work：0.2 sec


if __name__ == '__main__':
    x = depth()
    x.run_forever()

    a = {456.0: 32, 123.0: 64, 3.6: 7}
    b = {456.0: 32, 123.0: 2, 9: 16}
    # print(a)
    y = Util.sort_dict(a)
    z = DiffDict(a, b).get_diff()
    print("sort a y:", y)
    print("a:{},b:{},diff {}".format(a, b, z))

    file = Util.get_file_name("testa")
    Util.write_json_file(y, file)
    Util.write_json_file(z, file)
    j = Util.read_file(file)

    print("j:", j)
    loop = asyncio.get_event_loop()
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("interrupt end")
