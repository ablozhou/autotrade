import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor
import time
from pprint import pprint
import json

from util import Util
from tradedata import TradeData, TradeDataList
from kline import KLine
from strategy import Strategy

class Trade:
    '''Trade data process'''

    def __init__(self):
        self.SYMBOL = {"ETH-BTC": "ETH-BTC"}
        self.__rest_trade_url = "https://api.kucoin.com/v1/open/deal-orders"
        self.session = None
        self.last_data = None

        self.kline = KLine()
        self.stratege = Strategy(kline=self.kline)

    def run_forever(self):
        self.__loop = asyncio.new_event_loop()
        self.__executor = ThreadPoolExecutor(max_workers=2)
        self.__executor.submit(self.asyncio_initiator, self.__loop)
        asyncio.run_coroutine_threadsafe(self.trade_poller(symbol="ETH-BTC"), self.__loop)
        asyncio.run_coroutine_threadsafe(self.kline.minute_process(), self.__loop)

        while True:
            time.sleep(3)

    def asyncio_initiator(self, loop):
        asyncio.set_event_loop(loop=loop)
        loop.run_forever()

    async def trade_poller(self, symbol):
        self.session = aiohttp.ClientSession()
        last_data = None
        while True:
            async with self.session.get(url=self.__rest_trade_url, params={"symbol": symbol, "limit": 100},
                                        verify_ssl=True, proxy="http://127.0.0.1:1087") as response:
                json_data = await response.json()
                datas = []
                for data in json_data["data"]:
                    datas.append(TradeData(symbol, data))

                new_data_list, last_data = TradeDataList(datas, last_data).get_new_data()

                for new_data in new_data_list:
                    Util.write_json_file(new_data, Util.get_file_name("trade"))
                    self.kline.add_trade(new_data)
                    # 通知策略
                    self.stratege.trade1(new_data)



                await asyncio.sleep(3)  # work：0.2 sec


if __name__ == '__main__':
    x = Trade()
    x.run_forever()

    loop = asyncio.get_event_loop()
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("interrupt end")
