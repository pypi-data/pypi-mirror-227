from typing import Any


class ContainerBean:
    # 注册源
    register_source: str
    instance: Any
    name: str
    annotation_info: list
    clz: type
