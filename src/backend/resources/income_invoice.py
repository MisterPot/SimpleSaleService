from flask_restful import fields
from ..models import IncomeInvoice
from ..controller import InvoiceType
from .invoice_meta import create_invoice_resource
from ..utils import MoneyField


income_invoice_item_fields = {
    'id': fields.Integer,
    'product_id': fields.Integer,
    'sale_id': fields.Integer,
    'quantity': fields.Integer,
    'total_price': MoneyField,
    'arrival_date': fields.DateTime,
}


income_invoice_fields = {
    'id': fields.Integer,
    'date': fields.DateTime,
    'items': fields.List(fields.Nested(income_invoice_item_fields)),
    'total_price': MoneyField,
}


IncomeInvoiceResource, IncomeInvoiceSingleResource = create_invoice_resource(
    invoice_model=IncomeInvoice,
    invoice_type=InvoiceType.INCOME,
    name='IncomeInvoice',
    model_fields=income_invoice_fields
)
