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


class MarginIsolatedVipResult(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        
        class properties:
            dailyInterestRate = schemas.StrSchema
            discountRate = schemas.StrSchema
            level = schemas.StrSchema
            yearlyInterestRate = schemas.StrSchema
            __annotations__ = {
                "dailyInterestRate": dailyInterestRate,
                "discountRate": discountRate,
                "level": level,
                "yearlyInterestRate": yearlyInterestRate,
            }
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["dailyInterestRate"]) -> MetaOapg.properties.dailyInterestRate: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["discountRate"]) -> MetaOapg.properties.discountRate: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["level"]) -> MetaOapg.properties.level: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["yearlyInterestRate"]) -> MetaOapg.properties.yearlyInterestRate: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["dailyInterestRate", "discountRate", "level", "yearlyInterestRate", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["dailyInterestRate"]) -> typing.Union[MetaOapg.properties.dailyInterestRate, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["discountRate"]) -> typing.Union[MetaOapg.properties.discountRate, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["level"]) -> typing.Union[MetaOapg.properties.level, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["yearlyInterestRate"]) -> typing.Union[MetaOapg.properties.yearlyInterestRate, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["dailyInterestRate", "discountRate", "level", "yearlyInterestRate", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *args: typing.Union[dict, frozendict.frozendict, ],
        dailyInterestRate: typing.Union[MetaOapg.properties.dailyInterestRate, str, schemas.Unset] = schemas.unset,
        discountRate: typing.Union[MetaOapg.properties.discountRate, str, schemas.Unset] = schemas.unset,
        level: typing.Union[MetaOapg.properties.level, str, schemas.Unset] = schemas.unset,
        yearlyInterestRate: typing.Union[MetaOapg.properties.yearlyInterestRate, str, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'MarginIsolatedVipResult':
        return super().__new__(
            cls,
            *args,
            dailyInterestRate=dailyInterestRate,
            discountRate=discountRate,
            level=level,
            yearlyInterestRate=yearlyInterestRate,
            _configuration=_configuration,
            **kwargs,
        )
