import os.path

from flask import url_for
from flask_restful import Resource, reqparse
from ..controller import BusinessController
from ..report import (
    ReportType,
    RestOfProductReport,
    IncomeReport,
    SaleReport,
)

report_type_parser = reqparse.RequestParser()\
.add_argument(
    'report_type',
    dest='report_type',
    type=ReportType,

)

period_report_parser = reqparse.RequestParser()\
.add_argument(
    'start_time',
    dest='start_time',
    type=BusinessController.parse_time,
    location='json'
).add_argument(
    'end_time',
    dest='end_time',
    type=BusinessController.parse_time,
    location='json'
)

products_rest_parser = reqparse.RequestParser()\
.add_argument(
    'date',
    dest='date',
    type=BusinessController.parse_time,
    location='json'
)


class ReportResource(Resource):

    def post(self) -> str:
        report_type = report_type_parser.parse_args().report_type

        if report_type in [ReportType.INCOME, ReportType.SALE]:
            report_class = SaleReport if report_type == ReportType.SALE else IncomeReport
            arguments = period_report_parser.parse_args()
            path = report_class().create(**arguments)

        else:
            arguments = products_rest_parser.parse_args()
            path = RestOfProductReport().create(**arguments)

        return {'url': url_for('static', filename=f'reports/{os.path.basename(path)}')}
