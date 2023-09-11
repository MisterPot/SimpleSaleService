from typing import List

from flask import Response, make_response, request
from flask_restful import Resource, marshal_with_field, fields, marshal_with
from ..models import Product, db
from ..utils import MoneyField, with_count, Money


product_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'quantity': fields.Integer,
    'cost_price': MoneyField
}


def get_product_json() -> dict:
    """
    Help function, which converts arrived JSON to actual Product arguments
    :return:
    """

    product_in_json = request.json
    product_in_json['cost_price'] = Money.from_string(str(float(product_in_json['cost_price'])))

    for key in ['quantity', 'id']:
        if key in product_in_json:
            product_in_json.pop(key)

    return product_in_json


class ProductsResource(Resource):

    def options(self) -> Response:
        """
        Inform request for allow fetch data
        :return:
        """
        return make_response()

    @with_count(Product)
    @marshal_with_field(fields.List(fields.Nested(product_fields)))
    def get(self) -> List[Product]:
        return Product.query.all()

    @marshal_with(product_fields)
    def post(self) -> Product:
        product_in_json = get_product_json()
        product = Product(**product_in_json)
        db.session.add(product)
        db.session.commit()
        return product


class ProductSingleResource(Resource):

    def options(self, **_) -> Response:
        return make_response()

    @marshal_with(product_fields)
    def get(self, product_id: int) -> Product:
        return Product.query.filter(Product.id == product_id).first()

    @marshal_with(product_fields)
    def put(self, product_id: int) -> Product:
        product_in_json = get_product_json()
        product = Product.query\
            .filter(Product.id == product_id)
        product.update(product_in_json)
        db.session.commit()
        return product

    def delete(self, product_id: int) -> int:
        product = Product.query.get(product_id)
        db.session.delete(product)
        db.session.commit()
        return product_id
