# coding: utf-8

"""
    Bitget Open API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: 2.0.0
    Generated by: https://openapi-generator.tech
"""

from bitget.paths.api_margin_v1_cross_order_batch_cancel_order.post import MarginCrossBatchCancelOrder
from bitget.paths.api_margin_v1_cross_order_batch_place_order.post import MarginCrossBatchPlaceOrder
from bitget.paths.api_margin_v1_cross_order_cancel_order.post import MarginCrossCancelOrder
from bitget.paths.api_margin_v1_cross_order_fills.get import MarginCrossFills
from bitget.paths.api_margin_v1_cross_order_history.get import MarginCrossHistoryOrders
from bitget.paths.api_margin_v1_cross_order_open_orders.get import MarginCrossOpenOrders
from bitget.paths.api_margin_v1_cross_order_place_order.post import MarginCrossPlaceOrder


class MarginCrossOrderApi(
    MarginCrossBatchCancelOrder,
    MarginCrossBatchPlaceOrder,
    MarginCrossCancelOrder,
    MarginCrossFills,
    MarginCrossHistoryOrders,
    MarginCrossOpenOrders,
    MarginCrossPlaceOrder,
):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """
    pass
