from pathlib import Path

from flask import Flask
from flask_restful import Api
from flask_cors import CORS


app = Flask(__name__, static_folder=Path(__file__).parent / Path('static'))
api = Api(app)
sqlite_file = Path(__file__).parent / Path('test_database.sqlite')


CORS(app)
app.config.update(
    SECRET_KEY="A\xacE\x94\x04\x12\x93\xef\xa4\xea\xdd>\xff\t\x06\x00<\xb6J\xc6n\xba=\x02\xbb",
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    DEBUG=True,
    SQLALCHEMY_DATABASE_URI=f"sqlite:///{sqlite_file.as_posix()}",
)


from .resources.products import ProductsResource, ProductSingleResource
from .resources.consignments import ConsignmentsResource
from .resources.sale_invoice import SaleInvoiceResource, SaleInvoiceSingleResource
from .resources.income_invoice import IncomeInvoiceResource, IncomeInvoiceSingleResource
from .resources.reports import ReportResource
from .models import init_db


with app.app_context():

    api.add_resource(ProductsResource, '/products')
    api.add_resource(ProductSingleResource, '/products/<int:product_id>')

    api.add_resource(ConsignmentsResource, '/consignments')

    api.add_resource(SaleInvoiceResource, '/sale_invoices')
    api.add_resource(SaleInvoiceSingleResource, '/sale_invoices/<int:invoice_id>')

    api.add_resource(IncomeInvoiceResource, '/income_invoices')
    api.add_resource(IncomeInvoiceSingleResource, '/income_invoices/<int:invoice_id>')

    api.add_resource(ReportResource, '/report')

    init_db()
