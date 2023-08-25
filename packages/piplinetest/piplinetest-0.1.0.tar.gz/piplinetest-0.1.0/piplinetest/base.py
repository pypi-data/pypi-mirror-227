from dataclasses import dataclass, Field
from typing import Union, List, Type
from enum import Enum

from requests import Response

from .import_utils import import_lib
from .http_request import http_request


class TestStepTypeEnum(Enum):
    http_api = "http_api"
    ui = "ui"


@dataclass
class BaseTestStep(object):
    """base test step

    Args:
        BaseModel (_type_): every http test step
    """

    description: str = Field(description="接口描述", default=None)
    url: str = Field(description="接口请求地址")
    method: str = Field(description="接口请求方法")
    headers: Union[dict, None] = Field(description="接口请求头", default=None)
    body: Union[dict, str, list, None] = Field(description="请求body", default={})

    process_methods_prefix: str = Field(description="请求处理方法前缀", default=None)
    pre_process_method: Union[str, None] = Field(
        description="数据请求前处理方法路径", default=None
    )
    after_process_method: Union[str, None] = Field(
        description="数据请求后处理方法路径", default=None
    )

    def _send_request_data(self, request_dict: dict) -> Response:
        request_kwargs = {
            "http_url": request_dict["host"] + self.url,
            "method": self.method.value if self.method else None,
            "headers": self.headers,
        }
        if isinstance(self.body, (dict, list)):
            request_kwargs["json"] = self.body
        elif isinstance(self.body, str):
            request_kwargs["body"] = self.body
        else:
            pass

        return http_request(**request_kwargs)

    def execute(self, request_dict: dict):
        if self.pre_process_method is not None:
            pre_process_method = import_lib(
                self.process_methods_prefix + self.pre_process_method
            )
            self.body = pre_process_method(self.body)

        res = self._send_request_data(request_dict)

        if self.after_process_method is not None:
            after_process_method = import_lib(self.after_process_method)
            self.body = after_process_method(res.json())
        else:
            self.body = res.json()


@dataclass
class BasePipLineTest(object):
    """base test class

    Args:
        BaseModel (_type_): 完整的测试步骤
    """

    description: str = Field(description="测试描述", default=None)
    host: str = Field(description="请求地址")
    user_name: str = Field(description="用户名")
    password: str = Field(description="密码")
    total_execute_round: int = Field(description="总共运行次数", default=1)
    test_arguments: Union[dict, None] = Field(description="执行测试arguments", default=None)
    test_steps_list: List[Union[Type[BaseTestStep], None]] = Field(
        description="执行的单元测试列表", default=[]
    )

    def execute(self):
        init_dict = self.dict()
        for x in self.test_steps_list:
            if x is not None:
                per_test_step = x(body=init_dict)
                per_test_step.execute(init_dict)
                init_dict = per_test_step.body
        return init_dict
