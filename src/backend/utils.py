import functools
from typing import Union, Callable
import json

from flask_restful import fields
from flask import Response, make_response


class Money:

    """
    Represents a money in integer format
    """

    sign = u"\u20B4"
    decimals = 2

    def __init__(self, price: Union[int, str]):

        if isinstance(price, str):
            self.value = self.from_string(price=price)

        elif isinstance(price, int):
            self.value = price

        else:
            raise ValueError(f'Bad money type for value - {repr(price)}')

    @classmethod
    def from_string(cls, price: str) -> int:
        """
        Takes a price as integer from string
        :param price: price to take
        :return:
        """
        prefix, suffix = price.replace(cls.sign, '').replace(' ', '').split('.')
        extra_zeros = ''.join('0' for _ in range(cls.decimals - len(suffix)))
        suffix = suffix + extra_zeros if len(suffix) < cls.decimals else suffix
        return int(prefix) * (10 ** cls.decimals) + int(suffix[:cls.decimals])

    @classmethod
    def format_price(cls, price: int) -> str:
        """
        Formats price related to sign and decimals
        :param price: price to format
        :return:
        """
        return f'{price / (10 ** cls.decimals):0{cls.decimals}} {cls.sign}'

    def __str__(self):
        return self.format_price(price=self.value)


class MoneyField(fields.Raw, Money):

    """
    Field for marshal_with decorator
    ( easier serialization )
    """

    def format(self, value):
        return self.format_price(price=value)


def with_count(count_model: object) -> Callable:
    """
    Create Response and add to him additional count header

    :param count_model: from which model count will be taken
    :return:
    """
    def wrapper(fn) -> Callable:
        @functools.wraps(fn)
        def argument_wrapper(*args, **kwargs) -> Response:
            response = make_response()
            response.headers.update({
                'Access-Control-Expose-Headers': 'X-Total-Count',
                'X-Total-Count': count_model.query.count()
            })
            response.data = json.dumps(fn(*args, **kwargs))
            return response
        return argument_wrapper
    return wrapper
