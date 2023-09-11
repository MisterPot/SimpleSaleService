import datetime
import enum
from typing import (
    Union,
    List,
)

from .models import (
    db,
    SaleInvoice,
    SaleInvoiceItem,
    IncomeInvoice,
    IncomeInvoiceItem,
    Consignment,
    Product,
)
from .utils import Money


class InvoiceType(str, enum.Enum):
    INCOME = 'income'
    SALE = 'sale'


class BusinessController:

    """
    Controller, which controls entire service
    ( issue invoices, create consignments etc. )
    """

    @staticmethod
    def write_off_from_consignments(product: Product, to_write_off: int) -> None:
        """
        Writes off some quantity from product consignments.
        If consignment are fully writes off - marks as depreciated.
        :param to_write_off: quantity to write off
        :param product: product to write off
        :return:
        """
        current_to_write_off = to_write_off

        for consignment in product.consignments:

            current_cons_quantity = (
                0 if consignment.current_quantity <= current_to_write_off
                else consignment.current_quantity - current_to_write_off
            )

            if current_cons_quantity == 0:
                consignment.depreciated = True

            if consignment.current_quantity >= current_to_write_off:
                current_to_write_off = 0

            elif current_to_write_off > consignment.current_quantity:
                current_to_write_off -= consignment.current_quantity

            consignment.current_quantity = current_cons_quantity

            if current_to_write_off == 0:
                break

    @classmethod
    def create_sale_invoice(
            cls,
            date: datetime.datetime,
            invoice_items: List[SaleInvoiceItem]
    ) -> None:
        """
        Create a sale invoice with cargo subtraction
        from consignments
        :param date: invoice creation date
        :param invoice_items: items, which will be appended to this invoice
        :return:
        """
        invoice = SaleInvoice(date=date)

        for invoice_item in invoice_items:

            if invoice_item.quantity > invoice_item.product.quantity:
                raise ValueError('Current supply of product is lower than requested quantity')

            cls.write_off_from_consignments(
                product=invoice_item.product,
                to_write_off=invoice_item.quantity
            )

        invoice.items = invoice_items
        db.session.add_all(invoice_items)
        db.session.add(invoice)
        db.session.commit()

    @staticmethod
    def get_last_consignment(product: Product) -> Union[Consignment, None]:
        """
        Returns a last consignment of product.
        If product haven't consignments returns None
        :param product: product to check
        :return:
        """
        try:
            return product.consignments[-1]
        except IndexError:
            return

    @classmethod
    def create_income_invoice(
            cls,
            date: datetime.datetime,
            invoice_items: List[IncomeInvoiceItem]
    ) -> None:
        """
        Creates an income invoice and automatically manages a consignments
        :param date: invoice creation date
        :param invoice_items: items, which will be appended to this invoice and
        from which consignments will be made
        :return:
        """
        invoice = IncomeInvoice(date=date)
        consignments = []

        for invoice_item in invoice_items:

            last_consignment = cls.get_last_consignment(product=invoice_item.product)
            current_consignment_number = 1

            if last_consignment:
                current_consignment_number = last_consignment.consignment_number + 1

            consignments.append(
                Consignment(
                    consignment_number=current_consignment_number,
                    arrival_date=invoice_item.arrival_date,
                    quantity=invoice_item.quantity,
                    product=invoice_item.product,
                    current_quantity=invoice_item.quantity,
                    total_price=invoice_item.total_price,
                    income_invoice_item=invoice_item,
                )
            )

        invoice.items = invoice_items
        db.session.add_all(invoice_items)
        db.session.add_all(consignments)
        db.session.add(invoice)

        db.session.commit()

    @classmethod
    def create_invoice(
            cls,
            invoice_type: InvoiceType,
            creation_date: datetime.datetime,
            invoice_items: List[Union[IncomeInvoiceItem, SaleInvoiceItem]]
    ) -> None:
        """
        Creates new invoice of that type with items
        and save them
        :param creation_date: invoice creation date
        :param invoice_type: which invoice to create: 'sell' or 'income'
        :param invoice_items: items, which will be in that invoice items can't be []
        :return:
        """

        if len(invoice_items) == 0:
            raise ValueError('Invoice must contain at least one item')

        if invoice_type == InvoiceType.INCOME:
            cls.create_income_invoice(
                date=creation_date,
                invoice_items=invoice_items
            )

        elif invoice_type == InvoiceType.SALE:
            cls.create_sale_invoice(
                date=creation_date,
                invoice_items=invoice_items
            )
        else:
            raise ValueError('Unknown invoice type')

    @classmethod
    def create_item_from_json(cls, item_json: dict) -> Union[SaleInvoiceItem, IncomeInvoiceItem]:
        """
        Creating invoice item from json
        :param item_json: item in json format
        :return:
        """

        creation_class = SaleInvoiceItem

        if 'arrival_date' in item_json:
            creation_class = IncomeInvoiceItem
            item_json['arrival_date'] = cls.parse_time(item_json['arrival_date'])

        item_json['total_price'] = Money.from_string(str(float(item_json['total_price'])))

        product = Product.query.get(item_json['product_id'])

        return creation_class(**item_json, product=product)

    @staticmethod
    def parse_time(time_string: str) -> datetime.datetime:
        """
        Parsing time from string with corresponding format
        :param time_string: string to parse
        :return:
        """
        return datetime.datetime.strptime(time_string, '%Y-%m-%dT%H:%M:%S.%fZ')
