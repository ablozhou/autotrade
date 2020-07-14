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
# https://github.com/Kucoin/kucoin-api-docs

class depth:
    def __init__(self):
        self.SYMBOL = {"ETH-BTC": "ETH-BTC"}
        self.__rest_depth_url = "https://api.kucoin.com/api/v1/orders"
        self.session = None

        self.last_data = None

    def run_forever(self):
        self.__loop = asyncio.new_event_loop()
        self.__executor = ThreadPoolExecutor(max_workers=2)
        # 通过submit函数提交执行的函数到线程池中，submit函数立即返回，不阻塞. 但asyncio_initiator调用了forever(),会阻塞线程,所以该线程一直不返回
        task1 = self.__executor.submit(self.asyncio_initiator, self.__loop)
        # done方法用于判定某个任务是否完成
        print(task1.done())
        # result方法可以获取task的执行结果, 阻塞方法,如果没有结果会等待
        # print(task1.result())
        # cancel方法用于取消某个任务,该任务没有放入线程池中才能取消成功
        #print(task1.cancel())
        # asyncio.run_xxx 全部是阻塞的. run_coroutine_threadsafe 将协程线程安全的提交到event loop中.
        # 返回concurrent.futures.Future, 等待从操作系统的另一个线程中返回执行结果. 本例是死循环,所以不会返回
        asyncio.run_coroutine_threadsafe(self.depth_poller(symbol="ETH-BTC"),
                                         self.__loop)

        while True:
            time.sleep(3)

    def asyncio_initiator(self, loop):
        asyncio.set_event_loop(loop=loop)
        loop.run_forever()

    # 轮询获取深度信息的协程函数
    async def depth_poller(self, symbol):
        self.session = aiohttp.ClientSession()

        while True:
            async with self.session.get(
                    url=self.__rest_depth_url,
                    params={
                        "symbol": symbol,
                        "limit": 100
                    },
                    verify_ssl=False,
                    proxy="http://127.0.0.1:1087") as response:
                json_data = await response.json()

                data = DepthData(symbol, json_data)

                diff = DepthData.get_diff(data, self.last_data)

                self.last_data = data

                # 写redis或mongo或文件
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
