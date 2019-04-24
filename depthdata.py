from util import Util
from diff_dict import DiffDict


class DepthData():
    '''
    DepthData implement from dict and let d['a']['b'] equals to d.a.b
    It process depth data
    '''

    def __init__(self, symbol, data):
        self.t = data["timestamp"]  # TIME
        self.s = symbol  # SYMBO
        self.a = {}  # ASKS
        self.b = {}  # BIDS

        b = {}
        a = {}

        for price, quantity, amount in data["data"]["BUY"]:
            b[price] = quantity

        for price, quantity, amount in data["data"]["SELL"]:
            a[price] = quantity

        self.b = Util.sort_dict(b)
        self.a = Util.sort_dict(a)

    @staticmethod
    def get_diff(data, old_depth=None):
        diff = {}
        if old_depth is not None:
            diff["t"] = old_depth.t
            diff["s"] = old_depth.s
            diff["a"] = DiffDict(old_depth.a, data.a).get_diff()
            diff["b"] = DiffDict(old_depth.b, data.b).get_diff()
        else:
            diff = data
        return diff
