import importlib
import inspect
import json
import logging
import os
from typing import _AnnotatedAlias, Union, List
from ks_base.annotation import generate_bean_name, Source
from flask import Flask, request, send_from_directory, Blueprint

from ks_base.annotation import Autowire
from ks_base.container import ContainerBean

log = logging.getLogger(__name__)


class KsContainer:
    """
    submod and object container.
    """

    def __init__(self):
        # all submods
        self.submods: dict = {}
        # object container
        self.objects: dict[str, ContainerBean] = {}
        self.objects_with_class: dict[str, List[ContainerBean]] = {}
        # self.type_dict: dict[]
        log.info("HeeContainer init.")

    def get_obj_by_name(self, obj_name: str) -> Union[None, ContainerBean]:
        if obj_name in self.objects:
            return self.objects[obj_name]
        else:
            return None

    def get_obj_by_class(self, class_full_name: str) -> Union[None, List[ContainerBean]]:
        if class_full_name in self.objects_with_class:
            return self.objects_with_class[class_full_name]
        else:
            return None

    def get_submod_by_name(self, submod_name: str):
        if submod_name in self.submods:
            return self.submods[submod_name]


class KsApplication:
    flask: Flask
    env: str

    def __init__(self):
        self.ks_container = KsContainer()
        self.instantiate_context()
        self.scan_and_load_submod(".")
        # self.start_job_and_service()
        # self.scan_and_load_submod(".")
        # self.instantiate_objects()



        # 初始化环境
        # self.instantiate_env()
        # 初始化数据库
        # self.instantiate_db()

    def instantiate_context(self):
        from ks_base.context import context

        static_path = os.getcwd() + os.path.sep + 'static'
        log.info("static file path: " + static_path)
        self.flask = Flask(__name__, static_folder=static_path)
        context.set_app(self)



    def scan_and_load_submod(self, path):
        """
        """
        log.info("scan path: %s " % path)
        # Determine if it is a path, process the sub-path recursively
        if os.path.isdir(path):
            for subpath in os.listdir(path):
                log.info("subpath: %s" % subpath)

                if subpath.endswith('__pycache__'):
                    continue

                if subpath in ['.git', '.gitignore', '.idea', 'venv', 'application']:
                    continue

                self.scan_and_load_submod(path + "/" + subpath)

        # If it is a python file, load the processing module
        elif path.endswith(".py"):
            # All files under the root path are skipped
            if path.endswith('application.py') or path.endswith('manage.py'):
                return
            # Load all submods
            submod_full_name = path.replace("./", "").replace("/", ".").replace(".py", "")
            log.info('Load submod: ' + submod_full_name)
            submod = importlib.import_module(submod_full_name)

            # save submods
            self.ks_container.submods[submod_full_name] = submod
        else:
            log.info("skip path: %s" % path)

    def build_submod_dependencies(self):
        """
        各个模块注入依赖
        当所有对象被创建后,该方法会扫描Autowire注解,并注入实例对象
        """
        # Inject dependencies into submods
        log.info("Start to automatically inject dependencies into the submods.")
        for submod_name in self.ks_container.submods:
            submod = self.ks_container.submods[submod_name]
            # 自定注入依赖到子模块
            members = inspect.getmembers(submod)
            for m in members:
                if m[0] == '__annotations__':
                    annos = m[1]
                    for var_name in annos:
                        annotation = annos[var_name]

                        if isinstance(annotation, _AnnotatedAlias) is False:
                            continue

                        from typing import get_args
                        annotation_inner_list = get_args(annotation)
                        if len(annotation_inner_list) <= 1:
                            continue

                        annotation_instance = annotation_inner_list[1]
                        # 判断是否是autowire类型的注解
                        if isinstance(annotation_instance, Autowire):
                            # contained_object_name = var_type.__module__ + "." + var_type.__name__
                            bean_name = generate_bean_name(annotation_instance.name)
                            if bean_name in self.ks_container.objects:
                                setattr(submod, var_name, self.ks_container.objects[bean_name])
                                log.info(
                                    "Auto inject [" + bean_name + "] into submod " + submod_name + " success.")


class Web:
    """
    If you are building a web application, the web object will be injected into the controller when the controller is initialized. The web object provides the ability to process request parameters, request data acquisition, file download, upload, etc.
    """

    def __init__(self, flask: Flask):
        self.flask = flask

    def request_params(self):
        return request.args

    def request_data(self):
        return request.data

    def request_json(self):
        """
        请求json数据
        :return:
        """
        return json.loads(request.data)

    def request_files(self):
        """
        获取上传文件
        :return:
        """
        return request.files

    def resp_download(self, directory: str, file: str, **options):
        """
        响应返回下载文件
        :param directory:
        :param file:
        :param options:
        :return:
        """
        abs_download_dir = os.path.abspath(directory)
        # log_.info("abs_download_file: " + abs_download_dir)
        if not os.path.exists(abs_download_dir):
            return "file not existed!"
        else:
            return send_from_directory(abs_download_dir, file, **options)

    def resp_static_file(self, filename: str):
        """
        响应返回静态文件
        :param filename:
        :return:
        """
        return self.flask.send_static_file(filename)

    # def resp_json(self, data):
    #     """
    #     响应返回json数据。
    #         1. 自动将 datetime 类型数据转为yyyy-MM-dd HH:mm:ss类型。
    #         2. 自动将用户自定义类的对象转成json字符串，但以下划线打头的属性不进行转换。
    #     :param data:
    #     :return:
    #     """
    #     # 如果是用户自定义对象，则转成dict再序列化
    #     if str(type(data)).__contains__('.'):
    #         dict_data = object_to_dict(data)
    #         return json.dumps(dict_data, cls=HeeJsonEncoder)
    #     # 如果非用户自定义对象，则直接进行转换
    #     else:
    #         return json.dumps(data, cls=HeeJsonEncoder)


class KsRestApplication(KsApplication):
    """
    HeeRestApplication
    Used to build restful applications
    """

    def __init__(self):
        super(KsRestApplication, self).__init__()
        self.web = Web(self.flask)
        self.initialize_controller()
        # 对象注入
        self.build_submod_dependencies()




    def initialize_controller(self):
        """
        Map all controllers
        """
        log.info("Map all controllers.")
        for submod_name in self.ks_container.submods:
            if submod_name.endswith("controller"):
                submod = self.ks_container.submods[submod_name]
                if hasattr(submod, 'mapping'):
                    self.flask.register_blueprint(submod.mapping)

                if hasattr(submod, 'web'):
                    submod.web = self.web

    def start(self, host="127.0.0.1", port=5000, **kwargs):
        log.info("application is starting...")
        self.flask.run(host=host, port=port, **kwargs)


class KsWebApplication(KsRestApplication):
    def __init__(self, env):
        self.env = env
        self.initialize_default_dir()
        super(KsWebApplication, self).__init__()

    def initialize_default_dir(self):
        """
        Initialize all default paths of the project.
        If it is a web project, it will directly initialize a static path and template path to prevent static files and template files
        :return:
        """
        root_path = os.getcwd()
        if not os.path.exists(root_path + "/static/"):
            os.mkdir(root_path + "/static/")
            log.info("The static dir does not exists, create it.")


class Mapping(Blueprint):
    """
    Used to declare the request path, each controller needs to create an object of this type
    """

    def __init__(self, prefix: str):
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        submod_name = calframe[1][0].f_locals['__name__']
        name = submod_name.split(".")[-1]
        super(Mapping, self).__init__(name=name, import_name=submod_name, url_prefix=prefix)
