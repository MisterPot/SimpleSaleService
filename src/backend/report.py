import datetime
import enum
import os
import pathlib
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Any, Union, Tuple
import platform

from fpdf import FPDF
from sqlalchemy import func

from .models import (
    SaleInvoice,
    IncomeInvoice,
    IncomeInvoiceItem,
    SaleInvoiceItem,
    Product,
    Consignment,
    db
)
from .utils import Money


if platform.system() == 'Linux':
    pathlib.WindowsPath = pathlib.PosixPath


class Report(ABC):
    """
    Represents any report
    """

    @abstractmethod
    def serialize(self, *args, **kwargs) -> List[str]:
        """
        Serialize a report data to string format.
        This function uses for get pdf data
        :return:
        """

    @abstractmethod
    def get_filename(self, *args, **kwargs) -> str:
        """
        Must return a PDF filename to save in string format
        :return:
        """

    def create(self, *args, **kwargs) -> str:
        """
        Creates report from input data in PDF format.
        Path to file must be return as string
        :return:
        """

        pdf = FPDF()
        root = Path(__file__).parent
        font = root / Path('FreeSans.ttf')
        reports = root / Path('static') / Path('reports')
        filename = self.get_filename(*args, **kwargs)

        pdf.add_page()
        pdf.add_font('FreeSans', '', font, uni=True)
        pdf.set_font('FreeSans', '', size=15)

        for string in self.serialize(*args, **kwargs):
            pdf.write(10, string)

        prev_dir = os.getcwd()
        os.chdir(reports)
        pdf.output(filename)
        os.chdir(prev_dir)

        return reports / Path(filename)


def get_product_quantity_on_date(
        product_id: int,
        date: datetime.datetime
) -> int:
    """
    Help function, which get product quantity for certain date
    :param product_id: product id to check
    :param date: date, by which will sum
    :return:
    """
    total_income = db.session.query(func.sum(IncomeInvoiceItem.quantity)). \
        join(IncomeInvoiceItem.consignment). \
        join(Consignment.product). \
        filter(Product.id == product_id, IncomeInvoice.date <= date).scalar() or 0

    total_sales = db.session.query(func.sum(SaleInvoiceItem.quantity)). \
        join(SaleInvoiceItem.product). \
        filter(Product.id == product_id, SaleInvoice.date <= date).scalar() or 0

    current_quantity = total_income - total_sales

    return current_quantity if current_quantity > 0 else 0


class Formatter(ABC):
    """
    Abstract formatter, for any model
    """

    def __init__(self, item_to_format: Any):
        self.item_to_format = item_to_format

    @abstractmethod
    def format(self) -> str:
        """
        Returns formatted string depends
        on passed to __init__ string
        :return:
        """


class InvoiceFormatter(Formatter):
    item_to_format: Union[SaleInvoice, IncomeInvoice]

    def format(self) -> str:
        items = "\n".join([
            InvoiceItemFormatter(item).format()
            for item in self.item_to_format.items
        ])

        return (f'{self.item_to_format.__class__.__name__}#{self.item_to_format.id}\n'
                f'Creation date - {self.item_to_format.date.strftime("%Y/%m/%d %H:%M:%S")}\n'
                f'Items: \n'
                f'\n{items}')


class InvoiceItemFormatter(Formatter):
    item_to_format: Union[IncomeInvoiceItem, SaleInvoiceItem]

    def format(self) -> str:
        arrival_date = ''

        if getattr(self.item_to_format, 'arrival_date', None) is not None:
            arrival_date = f'---- Arrival date - {self.item_to_format.arrival_date.strftime("%Y/%m/%d %H:%M:%S")}\n'

        return (f'---- Product name - {self.item_to_format.product.name}\n'
                f'---- Total price - {Money.format_price(self.item_to_format.total_price)}\n'
                f'---- Quantity - {self.item_to_format.quantity}\n') + arrival_date


class ProductFormatter(Formatter):
    item_to_format: Product

    def __init__(self, date: datetime.datetime, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.date = date

    def format(self) -> str:
        date = self.date.strftime('%Y/%m/%d %H:%M:%S')
        date_quantity = get_product_quantity_on_date(
            product_id=self.item_to_format.id,
            date=self.date
        )
        return (f'---- Product name - {self.item_to_format.name}\n'
                f'---- Current quantity - {self.item_to_format.quantity}\n'
                f'---- Quantity for date {date} - {date_quantity}\n'
                f'---- Product price - {Money.format_price(self.item_to_format.cost_price)}\n')


class ModelPeriodicalReport(Report, ABC):
    """
    Represents a periodical report, which
    have a `start_time` - start of period
    and `end_time` - end of period.

    End of period can't be greater than start
    """

    __model__ = None

    REPORT_INDEX = 1

    def create(self, *args, **kwargs) -> str:
        path = super().create(
            start_time=kwargs['start_time'],
            end_time=kwargs['end_time'],
        )
        self.__class__.REPORT_INDEX += 1
        return path

    @staticmethod
    def get_dates(
            start_time: datetime.datetime,
            end_time: datetime.datetime
    ) -> Tuple[str, str]:
        """
        Help function for get stringed dates
        :return:
        """
        return start_time.strftime('%y_%m_%d'), end_time.strftime('%y_%m_%d')

    def get_filename(self, *args, **kwargs) -> str:
        start_time, end_time = self.get_dates(kwargs['start_time'], kwargs['end_time'])
        start_part = f'{self.__model__.__name__}Report{self.REPORT_INDEX}'
        filename = f"{start_part}_{start_time}_to_{end_time}.pdf"
        return filename

    def serialize(self, *args, **kwargs) -> List[str]:
        start_time = kwargs['start_time']
        end_time = kwargs['end_time']
        sales = self.__model__.query \
            .filter(self.__model__.date.between(start_time, end_time)) \
            .all()
        total_money = sum(sale.total_price for sale in sales)
        start_date, end_date = self.get_dates(start_time, end_time)
        formatted_sales = [InvoiceFormatter(sale).format() for sale in sales]
        return [
            f'Report{self.REPORT_INDEX}\n'
            f'From period {start_date} to {end_date}\n'
            f'Total money - {Money.format_price(total_money)}\n\n',
            *formatted_sales
        ]


class SaleReport(ModelPeriodicalReport):
    __model__ = SaleInvoice


class IncomeReport(ModelPeriodicalReport):
    __model__ = IncomeInvoice


class RestOfProductReport(Report):

    def create(self, *args, **kwargs) -> str:
        return super().create(date=kwargs['date'])

    def get_filename(self, *args, **kwargs) -> str:
        return f'ProductRestReport_{kwargs["date"].strftime("%y_%m_%d")}.pdf'

    def serialize(self, *args, **kwargs) -> List[str]:
        date = kwargs['date']
        products = '\n'.join([
            ProductFormatter(date=date, item_to_format=product).format()
            for product in Product.query.all()
        ])
        return [
            f'Report\n'
            f'Until the date - {date.strftime("%y_%m_%d")}\n\n',
            *products
        ]


class ReportType(str, enum.Enum):

    SALE = 'sale'
    INCOME = 'income'
    PRODUCT = 'product'
