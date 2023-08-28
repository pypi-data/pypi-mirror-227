import copy
from typing import Any, Union, List
import logging

from flask import Flask

from ks_base.utils import simple_util
from ks_base.container import ContainerBean

log = logging.getLogger(__name__)


class Context(object):
    app = None
    container = None
    influxdb = None

    def __init__(self):
        pass

    def set_app(self, app):
        self.app = app
        self.container = app.ks_container

    def get_flask(self) -> Union[Flask, None]:
        if self.app:
            return self.app.flask
        return None

    def set_influxdb(self, influxdb):
        self.influxdb = influxdb

    def get_influxdb(self):
        return self.influxdb

    def get_obj_by_name(self, name, renew=False) -> Union[ContainerBean, None]:
        bean: ContainerBean = self.container.get_obj_by_name(name)

        if bean is not None:
            if renew:
                return copy.deepcopy(bean.instance)
            return bean.instance
        return None

    def get_obj_by_class(self, class_name: str) -> Union[List[ContainerBean], None]:
        beans: List[ContainerBean] = self.container.get_obj_by_class(class_name)
        if beans is not None:
            return [bean.instance for bean in beans]
        return None

    def list_objs_with_type(self) -> dict[str, ContainerBean]:
        return self.container.objects_with_class

    def list_objs(self) -> dict[str, ContainerBean]:
        return self.container.objects

    def get_container(self):
        return self.container

    def instantiate_object(self, obj: any, alias=None, source=None) -> ContainerBean:
        """
        Instantiate all objects.
        """
        objs: dict[str, ContainerBean] = self.list_objs()
        objs_with_type: dict[str, ContainerBean] = self.list_objs_with_type()

        clz = obj.__class__

        name: str = alias if alias is not None else clz.__name__
        # name = name[0].lower() + name[1:]
        name = simple_util.get_bean_name(name)
        full_name = clz.__module__ + '.' + clz.__name__

        if name not in objs:
            log.info("contained object: " + full_name)
            bean = ContainerBean()
            bean.register_source = source
            bean.instance = obj
            bean.clz = clz
            bean.name = name
            objs[name] = bean

            beans = objs_with_type.get(full_name, [])
            beans.append(bean)
            objs_with_type[full_name] = beans

            log.info("name=" + name + ", object: " + obj.__str__())
            return bean
        return objs[name]


context = Context()
