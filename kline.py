from collections import deque

import asyncio
from datetime import datetime
import numpy as np

class KLine:
    '''k棒[O,H,L,C,T,V],open,high,low,close,time,volume, 开，高，低，收，时间，累计交易量。一分钟内收到trade数据就更新这个列表'''

    def __init__(self):
        self.kbar = [0, 0, 0, 0, 0, 0]
        self.deque = deque(maxlen=1440)
        self.side = 0  # 记录上一次收盘价在均价位置 1 上面，0 下面

    async def minute_process(self):  # one minute append to deque, and empty the kbar

        while True:
            self.deque.append(self.kbar)
            self.kbar = [0, 0, 0, 0, 0, 0]
            await asyncio.sleep(60 - datetime.now().second)  # sleep the same seconds as the nature time


    def add_trade(self, data):
        if self.kbar[0] == 0:  # first trade data
            self.kbar[0] = data.p  # open price
            self.kbar[1] = data.p  # high
            self.kbar[2] = data.p  # low
            self.kbar[3] = data.p  # close
            self.kbar[4] = data.t  # time
            self.kbar[5] = data.q  # volume
        else:
            if data.p > self.kbar[1]: # 如果超过最高价，则更新
                self.kbar[1] = data.p  # high
            if data.p < self.kbar[2]:
                self.kbar[2] = data.p  # low

            self.kbar[3] = data.p  # close
            self.kbar[4] = data.t  # time
            self.kbar[5] = self.kbar[5] + data.q  # volume

    def cross_over(self, close_price): # 是否穿过均线，给策略调用, 返回值 同一边0，向上穿越传1，向下穿越传-1.

        a = np.array(self.deque).T
        if len(a) == 0:
            return 0

        mean = np.sum(a[3][-20:])/len(a[3][-20:]) # 取20minute数据求均值

        if close_price > mean :
            if self.side == 1:  # 原来在上面，不变
                return 0
            else:  # 穿越向上
                self.side = 1
                return 1
        elif close_price < mean:
            if self.side == 0:  # 原来在下面，不变
                return 0
            else:  # 穿越向下
                self.side = 0
                return -1
        else:  # 在线上，认为不变
            return 0




