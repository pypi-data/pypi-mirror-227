from typing import Union, List, Any
from enum import Enum

from pydantic import BaseModel, Field
from requests import Response

from .import_utils import import_lib
from .http_request import http_request


class TestStepTypeEnum(Enum):
    http_api = "http_api"
    ui = "ui"


class BaseTestStep(BaseModel):
    """base test step

    Args:
        BaseModel (_type_): every http test step
    """

    name: str = Field(title="test step name", default=None)
    url: str = Field(title="http api url")
    method: str = Field(title="http method like: GET|POST|PATCH")
    headers: Union[dict, None] = Field(title="http header", default=None)
    body: Union[dict, str, list, None] = Field(title="http body", default={})

    process_methods_prefix: str = Field(
        title="process method import prefix", default=None
    )
    pre_process_method: Union[str, None] = Field(
        title="process method call before send http", default=None
    )
    after_process_method: Union[str, None] = Field(
        title="process method call after send http", default=None
    )

    def _send_request_data(self, request_dict: Union[dict, None]) -> Response:
        request_kwargs = {
            "http_url": request_dict["host"] + self.url,
            "method": self.method if self.method else None,
            "headers": self.headers,
        }
        if isinstance(self.body, (dict, list)):
            request_kwargs["json"] = self.body
        elif isinstance(self.body, str):
            request_kwargs["data"] = self.body
        else:
            pass

        return http_request(**request_kwargs)

    def execute(self, request_dict: Union[dict, None]):
        if self.pre_process_method is not None:
            pre_process_method = import_lib(
                self.process_methods_prefix + self.pre_process_method
            )
            self.body = pre_process_method(self.body)

        res = self._send_request_data(request_dict)

        if self.after_process_method is not None:
            after_process_method = import_lib(
                self.process_methods_prefix + self.after_process_method
            )
            self.body = after_process_method(res.json())
        else:
            self.body = res.json()


class BasePipLineTest(BaseModel):
    """base test class"""

    name: str = Field(title="test name", default=None)
    host: str = Field(title="http host")
    total_execute_round: int = Field(title="total execute round", default=1)
    test_arguments: Union[dict, None] = Field(title="execute arguments", default=None)
    test_steps_list: List[Union[Any, None]] = Field(
        title="test step lists to execute", default=[]
    )

    def execute(self):
        init_dict = self.dict()
        # init_dict.pop("test_steps_list")
        for x in self.test_steps_list:
            if x is not None:
                per_test_step = x()
                per_test_step.execute(init_dict)
                init_dict = per_test_step.body
        return init_dict
