from util import Util
from diff_dict import DiffDict


class TradeData:
    '''
    TradeData implement from dict and let d['a']['b'] equals to d.a.b
    It process trade data
    '''

    def __init__(self, symbol, data):
        self.t = data[0]  # TIME
        self.s = symbol  # SYMBOL
        self.dir = data[1]  # direction string: buy,sell
        self.p = data[2]  # price
        self.q = data[3]  # quantity
        self.id = data[5]  # trade id,a hash


class TradeDataList:

    def __init__(self, trade_datas: list, last_data: dict = None):
        self.trade_datas = trade_datas
        self.trade_datas_new = []
        self.last_data = last_data

    def get_new_data(self):
        ''' return (self.trade_datas_new, self.max_data )'''
        # 便利，找到比较新的，存到self.trade_datas_new，并且找到集合中最大的时间戳的数据，留给下一次比较时用
        if self.last_data is not None:
            for d in self.trade_datas:

                if d.t > self.last_data["t"]:  # 比最后的数据新
                    self.trade_datas_new.append(d)
                    self.last_data["t"] = d.t if d.t > self.last_data["t"] else self.last_data["t"]
                    self.last_data["id"] = {d.id}
                elif d.t == self.last_data["t"] and (d.id not in self.last_data["id"]): # 时间相等，id不等，则是新的
                    self.trade_datas_new.append(d)
                    self.last_data["id"].add(d.id)

        else: # 第一条数据
            self.trade_datas_new = self.trade_datas
            self.last_data={}
            self.last_data["t"] = self.trade_datas[0].t
            self.last_data["id"]=set()
            for d in self.trade_datas:
                if d.t > self.last_data["t"]:
                    self.last_data["t"] = d.t
                    self.last_data["id"] = {d.id}
                elif d.t == self.last_data["t"]:
                    self.last_data["id"].add(d.id)

        return self.trade_datas_new, self.last_data
