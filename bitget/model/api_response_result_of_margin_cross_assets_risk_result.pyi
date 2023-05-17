# coding: utf-8

"""
    Bitget Open API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: 2.0.0
    Generated by: https://openapi-generator.tech
"""

from datetime import date, datetime  # noqa: F401
import decimal  # noqa: F401
import functools  # noqa: F401
import io  # noqa: F401
import re  # noqa: F401
import typing  # noqa: F401
import typing_extensions  # noqa: F401
import uuid  # noqa: F401

import frozendict  # noqa: F401

from bitget import schemas  # noqa: F401


class ApiResponseResultOfMarginCrossAssetsRiskResult(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        
        class properties:
            code = schemas.StrSchema
        
            @staticmethod
            def data() -> typing.Type['MarginCrossAssetsRiskResult']:
                return MarginCrossAssetsRiskResult
            msg = schemas.StrSchema
            requestTime = schemas.Int64Schema
            __annotations__ = {
                "code": code,
                "data": data,
                "msg": msg,
                "requestTime": requestTime,
            }
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["code"]) -> MetaOapg.properties.code: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["data"]) -> 'MarginCrossAssetsRiskResult': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["msg"]) -> MetaOapg.properties.msg: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["requestTime"]) -> MetaOapg.properties.requestTime: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["code", "data", "msg", "requestTime", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["code"]) -> typing.Union[MetaOapg.properties.code, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["data"]) -> typing.Union['MarginCrossAssetsRiskResult', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["msg"]) -> typing.Union[MetaOapg.properties.msg, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["requestTime"]) -> typing.Union[MetaOapg.properties.requestTime, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["code", "data", "msg", "requestTime", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *args: typing.Union[dict, frozendict.frozendict, ],
        code: typing.Union[MetaOapg.properties.code, str, schemas.Unset] = schemas.unset,
        data: typing.Union['MarginCrossAssetsRiskResult', schemas.Unset] = schemas.unset,
        msg: typing.Union[MetaOapg.properties.msg, str, schemas.Unset] = schemas.unset,
        requestTime: typing.Union[MetaOapg.properties.requestTime, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'ApiResponseResultOfMarginCrossAssetsRiskResult':
        return super().__new__(
            cls,
            *args,
            code=code,
            data=data,
            msg=msg,
            requestTime=requestTime,
            _configuration=_configuration,
            **kwargs,
        )

from bitget.model.margin_cross_assets_risk_result import MarginCrossAssetsRiskResult
