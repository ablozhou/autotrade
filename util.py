import json
import time


class Util:

    # sort data of items
    @staticmethod
    def sort_dict(d):
        # using  sorted(d.items(), key=lambda item: item[0]) turn to list(tuples,...)# 转为元组，不符合要求
        return {p: d[p] for p in sorted(d.keys(), reverse=False)}

    @staticmethod
    def read_file(json_file, encoding="utf-8"):
        with open(json_file, "r", encoding=encoding) as fp:
            return fp.readlines()

    @staticmethod
    def write_json_file(obj, json_file:str, encoding="utf-8"):
        j = json.dumps(Util.obj2dict(obj), ensure_ascii=False)  # 有中文 填入ensure_ascii=False
        with open(json_file, "a") as fp:
            fp.write(j)
            fp.write("\n")

    @staticmethod
    def read_last_json_line(json_file,encoding="utf-8"):
        with open(json_file, "r", encoding=encoding) as fp:
            fp.seek(-3,2) # seek(offset,whence),offset大于0，往后offset个字符，<0 往前。whence=0,from begin,1 from current,2 from end
            last_line = fp.readline()
            return json.load(last_line)

    @staticmethod
    def get_date(fmt="%Y-%m-%d"):
        return time.strftime(fmt, time.localtime(time.time()))

    @staticmethod
    def get_file_name(prefix, postfix=".json"):
        return prefix + Util.get_date() + postfix

    @staticmethod
    def obj2dict(obj):

        if obj:
            if isinstance(obj,dict):
                return obj
            else:
                obj_dict={}
                obj_dict.update(obj.__dict__)
                return obj_dict
        else:
            return {}
