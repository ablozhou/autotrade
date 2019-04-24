class DiffDict:
    '''b相对于a增加的key，修改的value和消失的key，都作为一个dict返回。消失的key，其value为0'''

    def __init__(self, old: dict, new_dict: dict = None):
        self.old_dict = old
        self.new_dict = new_dict
        self.d = {}  # diff
        self.added = {}
        self.removed = {}
        self.changed = {}
        self.a_key_set = set(old.keys())
        self.b_key_set = set(new_dict.keys())
        self.intersect_keys = self.a_key_set & self.b_key_set

    def get_added(self):
        if self.new_dict is None:
            self.added = {}
        else:
            self.added = {k: self.new_dict[k] for k in self.new_dict.keys() if k not in self.old_dict.keys()}
        return self.added

    def get_rm(self):
        if self.new_dict is None:
            self.removed={}
        else:
            self.removed = {k: 0 for k in self.old_dict.keys() if k not in self.new_dict.keys()}
        return self.removed

    def get_chg(self):
        if self.new_dict is None:
            self.changed = {}
        else:
            self.changed = {k: self.old_dict[k] for k in self.intersect_keys if self.old_dict[k] != self.new_dict[k]}
        return self.changed

    def get_diff(self):
        a = self.get_added()
        r = self.get_rm()
        c = self.get_chg()
        self.d = {**a, **c, **r}
        return self.d


if __name__ == '__main__':
    a = {6: 5, 5: 7, 3: 2}
    b = {6: 5, 5: 8, 9: 10, 11: 8}
    x = DiffDict(a, b)
    y = x.get_diff()
    print(y)
