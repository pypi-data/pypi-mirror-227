import inspect
from typing import get_args, _AnnotatedAlias, Any
import logging

from decimal import Decimal
from datetime import datetime
from ks_base.constant import content_type
from ks_base.utils import date_util
from ks_base.container import ContainerBean
from ks_base.context import context
from flask import has_request_context

log = logging.getLogger(__name__)


class RequestBody:
    """
    请求吃实话
    """

    def __init__(self, msg_type=content_type.application_json):
        self.msg_type = msg_type

    def parse(self, tp: type, val) -> Any:
        if val is None:
            return None
        if tp == float:
            return float(val)
        if tp == int:
            return int(val)
        if tp == datetime:
            return date_util.try_parse(val)

    def __call__(self, f):
        """
        被RequestBody装饰的方法会执行wrap内的方法
        f 被装饰的方法
        """

        def wrap(*args, **kwargs):
            # 获取被装饰方法的所有参数
            sign = inspect.signature(f)
            func_args = {}
            allow_all_param_match: bool = False
            for param in sign.parameters.values():
                name = param.name
                tp: type = param.annotation

                if param.name == 'self':
                    continue

                if param.name == 'kwargs':
                    allow_all_param_match = True
                    continue

                if isinstance(tp, _AnnotatedAlias):
                    annotation_list = get_args(tp)
                    # 被typing.Annotated包裹的类型，额外添加了参数的别名
                    alias: Alias = annotation_list[1]
                    default = param.default
                    if callable(default):
                        default = default()

                    tp: type = annotation_list[0]
                    func_args[name] = self.parse(tp, kwargs.get(alias.name, default))

            if allow_all_param_match:
                diffs = list(set(kwargs.keys()).difference(set(func_args.keys())))
                for diff in diffs:
                    func_args[diff] = kwargs.get(diff)

            result = f(*args, **func_args)
            return result

        return wrap


class Source:
    def __init__(self, alias=None):
        self.alias = alias

    def __call__(self, clz):
        obj = clz()
        bean: ContainerBean = context.instantiate_object(obj, alias=self.alias, source=Source.__name__)
        obj.name = bean.name
        clz_desc = None if clz.__doc__ is None else clz.__doc__.strip()

        # from app.main.script.hblg import init_variable_sql
        # init_variable_sql.insert(bean.name, clz_desc)

        def wrap(*args, **kwargs):
            # print('执行wrap()')
            # print('装饰器参数：', self.arg1, self.arg2)
            # print('执行' + f.__name__ + '()')
            # clz(*args, **kwargs)
            return bean.instance
            # print(f.__name__ + '()执行完毕')

        return wrap


class Component:

    def __init__(self):
        pass

    def __call__(self, f):
        context.instantiate_objects(f, source=Component.__name__)

        def wrap(*args, **kwargs):
            f(*args, **kwargs)

        return wrap


class FlaskContext:
    def __init__(self):
        pass

    def __call__(self, f):
        def wrap(*args, **kwargs):
            # 当前已经在上下文中，直接执行方法
            if has_request_context():
                result = f(*args, **kwargs)
                return result
            else:
                flask = context.get_flask()
                if flask:
                    with flask.app_context():
                        result = f(*args, **kwargs)
                        return result

        return wrap


class Invoke:
    use_cache: bool = False

    def __init__(self, use_cache=False):
        self.use_cache = use_cache

    def __call__(self, f):
        """
        被Invoke装饰的方法会执行wrap内的方法
        """

        def wrap(*args, **kwargs):
            # print('执行wrap()')
            # print('装饰器参数：', self.arg1, self.arg2)
            result = None
            if self.use_cache:
                # 获取缓存
                pass
            try:
                result = f(*args, **kwargs)
                return_type = f.__annotations__["return"]
                if return_type is not None \
                        and type(result) != return_type \
                        and result is not None:
                    result = return_type(result)
            except Exception as e:
                log.error(e, exc_info=True)
            if self.use_cache and result is not None:
                # 保存缓存
                pass
            if result is None:
                class_full_name = f.__module__ + "." + f.__qualname__.split('.')[0]
                r = context.get_obj_by_class(class_full_name)
                result = r[0].get_default()
            if isinstance(result, float):
                if abs(result) > 0.01:
                    result = float(Decimal(result).quantize(Decimal("0.01"), rounding="ROUND_HALF_UP"))
                elif abs(result) > 0.0001:
                    result = float(Decimal(result).quantize(Decimal("0.0001"), rounding="ROUND_HALF_UP"))
            return result

        wrap.annotation = Invoke
        wrap.method = f
        return wrap


class Alias:
    """
    别名标注
    """

    def __init__(self, name):
        self.name = name


class JSONField:
    def __init__(self, format):
        self.format = format


class Autowire:
    """
    用作依赖注入的对象的标注
    """

    # @classmethod
    # def __getitem__(self, item) -> T:
    #     return self.list[item]

    def __init__(self, name):
        self.name = name

    def get_origin_class(self):
        """
        获取其中的泛型类
        """
        c = get_args(self.__orig_class__)[0]
        return c

    def __(self):
        """
        获取其中的泛型类
        """
        c = get_args(self.__orig_class__)[0]
        return c


def generate_bean_name(name: str) -> str:
    """
    模仿spring的明明方式
    """
    head: str = name[0:2]
    if head.isupper():
        return name
    else:
        return name[0].lower() + name[1:]


def Component(cls):
    """
    Component annotation, the annotated class will be automatically instantiated in the container,
    and the instantiated object will be automatically injected when the submodule is initialized.
    """
    obj = cls()
    context.instantiate_object(obj, source=Component.__name__)
    return cls
