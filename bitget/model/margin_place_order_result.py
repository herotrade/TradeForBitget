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


class MarginPlaceOrderResult(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        
        class properties:
            clientOid = schemas.StrSchema
            orderId = schemas.StrSchema
            __annotations__ = {
                "clientOid": clientOid,
                "orderId": orderId,
            }
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["clientOid"]) -> MetaOapg.properties.clientOid: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["orderId"]) -> MetaOapg.properties.orderId: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["clientOid", "orderId", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["clientOid"]) -> typing.Union[MetaOapg.properties.clientOid, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["orderId"]) -> typing.Union[MetaOapg.properties.orderId, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["clientOid", "orderId", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *args: typing.Union[dict, frozendict.frozendict, ],
        clientOid: typing.Union[MetaOapg.properties.clientOid, str, schemas.Unset] = schemas.unset,
        orderId: typing.Union[MetaOapg.properties.orderId, str, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'MarginPlaceOrderResult':
        return super().__new__(
            cls,
            *args,
            clientOid=clientOid,
            orderId=orderId,
            _configuration=_configuration,
            **kwargs,
        )
