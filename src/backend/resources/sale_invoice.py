from flask_restful import fields
from ..controller import InvoiceType
from ..models import SaleInvoice
from ..utils import MoneyField
from .invoice_meta import create_invoice_resource


sale_invoice_item_fields = {
    'id': fields.Integer,
    'product_id': fields.Integer,
    'sale_id': fields.Integer,
    'quantity': fields.Integer,
    'total_price': MoneyField,
}


sale_invoice_fields = {
    'id': fields.Integer,
    'date': fields.DateTime,
    'items': fields.List(fields.Nested(sale_invoice_item_fields)),
    'total_price': MoneyField,
}


SaleInvoiceResource, SaleInvoiceSingleResource = create_invoice_resource(
    model_fields=sale_invoice_fields,
    invoice_type=InvoiceType.SALE,
    invoice_model=SaleInvoice,
    name='SaleInvoice'
)
