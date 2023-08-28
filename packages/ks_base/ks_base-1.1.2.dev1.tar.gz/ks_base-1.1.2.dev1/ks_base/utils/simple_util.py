# coding=utf-8
import importlib
import os
import hashlib
from decimal import Decimal
import datetime
import logging as log


def is_basic_type(tp: type) -> bool:
    return tp in [int, float, str]


def get_bean_name(name) -> str:
    """
    获得spring的命名方式的名称
    """
    head: str = name[0:2]
    if head.isupper():
        return name
    else:
        return name[0].lower() + name[1:]


def get_root_path():
    """
    获取项目根路径
    :return:
    """
    basedir = os.path.abspath(os.path.dirname(__file__))
    root_path = basedir[:basedir.find('app')]

    return root_path


def get_method_by_path(path):
    p, m = path.rsplit('.', 1)
    log.info("module {} m {}".format(p, m))
    method = getattr(importlib.import_module(p),
                     m, None)
    return method


def group(targets: list, k):
    g = {}
    for target in targets:
        collection = g.get(target[k], [])
        collection.append(target)
        g[target[k]] = collection
    return g


def is_not_empty(b: str):
    return b != None and b != ''


def is_empty(b: str):
    if b is None: return True
    return b == ''


def list_file(rootdir, absolute=True):
    """
    列出rootdir下的所有文件
    :param rootdir: 根路径
    :param absolute: 是否展示绝对路径,如果为False,那么展示基于rootdir的相对路径
    :return: list of file path
    """
    list = []
    __list(rootdir, list)

    if absolute is False:
        list = map(lambda x: x.replace(rootdir + "/", ""), list)

    return list


def __list(rootdir, list):
    """
    listFile的字方法,用于递归调用
    :param rootdir: 根路径
    :param list: list of file path
    :return:
    """
    for root, dirs, files in os.walk(rootdir):  # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
        for dirname in dirs:
            __list(dirname, list)

        for filename in files:
            list.append(os.path.join(root, filename))


def is_num(v):
    """
    判断v是否为数字
    :param v:
    :return:
    """
    try:
        val = float(v)
        return True
    except ValueError:
        return False


def float_nan_to_str_nan(x):
    """
    float类型的nan转换为字符串
    :param x:
    :return:
    """
    if type(x) == float:
        return str(x)
    else:
        return x


def to_md5(str):
    """
    md5加密
    :param str: 被加密的字符串
    :return:  密文
    """
    m = hashlib.md5()
    m.update(str)
    s = m.hexdigest()
    return s


def get_file_size(file_path):
    """
    根据路径获得文件的大小
    :param file_path:
    :return:
    """
    byte_size = os.path.getsize(file_path)
    return to_file_size(byte_size)


def to_file_size(byte_size):
    unit = 1024
    if byte_size < unit:
        return byte_size + 'B'
    elif (byte_size >> 10) < unit:
        return str(round(Decimal(byte_size / 1024.0), 1)) + 'K'
    elif (byte_size >> 20) < unit:
        return str(round(Decimal(byte_size / 1024.0 / 1024.0), 1)) + 'M'
    else:
        return str(round(Decimal(byte_size / 1024.0 / 1024.0 / 1024.0), 1)) + 'G'


def query_to_base(query, custom_field=None):
    """
    sqlalchemy的query对象转换为基础的list和dict

    """

    fields = []
    if len(query.all()) > 0:
        example = query.first()
        attrs = [x for x in dir(example) if
                 in_custom_field(x, example, custom_field)]

        # 检索结果集的行记录
        for rec in query.all():
            # 检索记录中的成员
            record = {}
            for field in attrs:
                # 定义一个字典对象
                data = rec.__getattribute__(field)

                if isinstance(data, datetime.datetime):
                    record[field] = data.isoformat(sep=" ")
                else:
                    record[field] = data
                    # elif isinstance(data, datetime.date):
                    #     record[field] = data.isoformat()
                    # elif isinstance(data, datetime.timedelta):
                    #     record[field] = (datetime.datetime.min + data).time().isoformat()
            # if len(query.all()) == 1:
            #     return record
            fields.append(record)
            # 返回字典数组
    return fields


def model_to_base(model, custom_field=None):
    """
    将数据库记录对象转换为基础类型
    :param model: sqlAlchemy对象
    :param custom_field: 指定转换的字段
    :return: 单个对象以dict返回,多个对象以list形式的dict返回
    """
    if isinstance(model, list):
        fields = list()
        if len(model) > 0:
            example = model[0]
            # 判断是否为model类型
            if isinstance(example, TableBase) is not True:
                return model
            attrs = [x for x in example.__dict__.keys() if
                     in_custom_field(x, example, custom_field)]
            for m in model:
                record = dict()
                for field in attrs:
                    # 定义一个字典对象
                    data = m.__getattribute__(field)
                    # if isinstance(data, datetime.datetime):
                    #     record[field] = data.isoformat(sep=" ")
                    # else:
                    record[field] = data
                    # elif isinstance(data, datetime.date):
                    #     record[field] = data.isoformat()
                    # elif isinstance(data, datetime.timedelta):
                    #     record[field] = (datetime.datetime.min + data).time().isoformat()
                    # if len(query.all()) == 1:
                    #     return record
                fields.append(record)
        return fields
    else:
        if isinstance(model, TableBase) is not True:
            return model
        attrs = [x for x in dir(model) if
                 in_custom_field(x, model, custom_field)]
        record = dict()
        for field in attrs:
            # 定义一个字典对象
            data = model.__getattribute__(field)

            if isinstance(data, datetime.datetime):
                record[field] = data.isoformat(sep=" ")
            else:
                record[field] = data
                # elif isinstance(data, datetime.date):
                #     record[field] = data.isoformat()
                # elif isinstance(data, datetime.timedelta):
                #     record[field] = (datetime.datetime.min + data).time().isoformat()
                # if len(query.all()) == 1:
                #     return record
        return record


def result_dict(result):
    if isinstance(result, list):
        fields = list()
        if len(result) > 0:
            example = result[0]
            attrs = [x for x in dir(example) if
                     in_custom_field(x, example, None)]
            for m in result:
                record = dict()
                for field in attrs:
                    data = m.__getattribute__(field)
                    record[field] = data
                fields.append(record)
        return fields
    else:
        attrs = [x for x in dir(result) if
                 in_custom_field(x, result, None)]
        record = dict()
        for field in attrs:
            data = result.__getattribute__(field)
            if isinstance(data, datetime.datetime):
                record[field] = data.isoformat(sep=" ")
            else:

                record[field] = data
        return record





def in_custom_field(x, example, custom_field):
    if custom_field is None:
        if not x.startswith('_') \
                and hasattr(example.__getattribute__(x), '__call__') == False \
                and x != 'metadata' \
                and x != 'query':
            return True
    elif x in custom_field:
        return True
    return False


def copy_properties(origin, dest):
    if dest is None or origin is None:
        return None
    if isinstance(origin, dict):
        attrs = origin.keys()
        for field in attrs:
            if hasattr(dest, field):
                data = origin.get(field)
                dest.__setattr__(field, data)
    else:
        attrs = [x for x in dir(origin)]
        for field in attrs:
            if not field.startswith('_'):
                if hasattr(dest, field):
                    data = origin.__getattribute__(field)
                    dest.__setattr__(field, data)


def obj2dict(obj):
    # convert object to a dict
    d = dict()
    d['__class__'] = obj.__class__.__name__
    d['__module__'] = obj.__module__
    d.update(obj.__dict__)
    return d


def dict2obj(dict):
    if '__class__' in dict:
        class_name = dict.pop('__class__')
        module_name = dict.pop('__module__')
        module = __import__(module_name)
        class_ = getattr(module, class_name)
        args = dict((key.encode('ascii'), value) for key, value in dict.items())
        inst = class_(**args)
    else:
        inst = dict
    return inst


def row_to_dict(row_list):
    result = []
    for row in row_list:
        result.append(dict(row._mapping))
    return result


def dictToObj(results, to_class):
    """将字典list或者字典转化为指定类的对象list或指定类的对象
    python 支持动态给对象添加属性，所以字典中存在而该类不存在的会直接添加到对应对象
    """
    if isinstance(results, list):
        objL = []
        for result in results:
            obj = to_class()
            for r in result.keys():
                obj.__setattr__(r, result[r])
            objL.append(obj)
        return objL
    elif isinstance(results, dict):
        obj = to_class()
        for r in results.keys():
            obj.__setattr__(r, results[r])
        return obj
    else:
        print("传入对象非字典或者list")
        return None


def parse_seconds(time):
    if time is None:
        return 300
    t = int(time[:-1])
    if "h" in time:
        return 60 * 60 * t
    elif "m" in time:
        return 60 * t
    elif "s" in time:
        return t


def drictToStrStock(nowData, tableName):
    sql1 = "insert into " + tableName + " ("
    sql2 = " values ("
    retData = ""
    retList = []
    for k in nowData:
        retData = ""
        sql1 = "insert into " + tableName + " ("
        sql2 = " values ("
        for i, j in k.items():
            sql1 += str(i)
            sql1 += ","
            if (type(j) is str):
                sql2 += '\'' + str(j) + '\''
            else:
                sql2 += str(j)
            sql2 += ","
        sql1 = sql1[0:-1] + ")"
        sql2 = sql2[0:-1] + ")"
        retData = sql1 + sql2
        retList.append(retData)
    return retList


if __name__ == "__main__":
    # print(drictToStrStock([dict(name=1,sex=2)],"table"))
    # import pandas as pd
    # p = pd.DataFrame([dict(a=123),dict(a=12),dict(a=321),dict(a=43),dict(a=123),dict(a=123)])
    # p[0:2].reset_index(drop=True).to_excel("./a.xlsx",index=False)
    # p[2:4].reset_index(drop=True).to_excel("./b.xlsx",index=False)
    print(get_root_path())



