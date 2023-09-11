from typing import List

from flask import Response, make_response
from flask_restful import Resource, marshal_with_field, fields
from ..models import Consignment
from ..utils import with_count, MoneyField


consignment_fields = {
    'id': fields.Integer,
    'consignment_number': fields.Integer,
    'arrival_date': fields.DateTime,
    'product_id': fields.Integer,
    'quantity': fields.Integer,
    'current_quantity': fields.Integer,
    'depreciated': fields.Boolean,
    'total_price': MoneyField
}


class ConsignmentsResource(Resource):

    def options(self) -> Response:
        return make_response()

    @with_count(Consignment)
    @marshal_with_field(fields.List(fields.Nested(consignment_fields)))
    def get(self) -> List[Consignment]:
        return Consignment.query.all()
