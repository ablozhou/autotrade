from kline import KLine
from tradedata import TradeData


# 柜台，和交易所连接
# 保存订单信息，用于撤单，排序自己的订单簿。不同的类可以触发不同的条件
class Strategy:

    def __init__(self, kline=None, depth=None):
        self.kline = kline
        self.depth = depth

    def set_kline(self,kline):
        self.kline = kline

    def set_depth(self,depth):
        self.depth=depth

    # depth 盘口变化 callback，深度驱动
    def depth1(self,data):
        # 刷量交易，同时发两个，一个挂单，一个吃单。挂单价格是买1和卖1之间的价格。如果上面有大卖单，则不好拉。否则可以花很小的代价，拉升价格。
        print(data)

    # trade 变为，callback 交易驱动
    def trade1(self, data: TradeData):
        # 根据策略，如果交易发生变化时，自成交发生变化

        c = self.kline.cross_over(data.p)
        if c > 0 : #  上穿
            print("上穿策略")
        elif c < 0 : # 下穿
            print("下穿策略")
