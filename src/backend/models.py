from sqlalchemy import event
from sqlalchemy.ext.hybrid import hybrid_property
from flask_sqlalchemy import SQLAlchemy

from .app import app


with app.app_context():
    db = SQLAlchemy(app, session_options={'autoflush': False})


class Product(db.Model):
    """
    Represents a product in admin page
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    cost_price = db.Column(db.Integer, nullable=False)

    consignments = db.relationship(
        'Consignment',
        backref='product',
        cascade='all, delete-orphan'
    )

    sale_invoice_items = db.relationship(
        'SaleInvoiceItem',
        backref='product',
        cascade='all, delete-orphan'
    )

    income_invoice_items = db.relationship(
        'IncomeInvoiceItem',
        backref='product',
        cascade='all, delete-orphan'
    )

    @hybrid_property
    def quantity(self) -> int:
        return sum(map(lambda consignment: consignment.current_quantity, self.consignments))


class IncomeInvoice(db.Model):
    """
    Invoice, which will
    """

    __tablename__ = 'income_invoice'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)

    items = db.relationship(
        'IncomeInvoiceItem',
        backref='income_invoice',
        lazy=True,
        cascade='all, delete-orphan'
    )

    @hybrid_property
    def total_price(self) -> int:
        return sum(map(lambda item: item.total_price, self.items))


class IncomeInvoiceItem(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id', ondelete='CASCADE'), nullable=False)
    invoice_id = db.Column(db.Integer, db.ForeignKey('income_invoice.id', ondelete='CASCADE'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    arrival_date = db.Column(db.DateTime, nullable=False)
    total_price = db.Column(db.Integer, nullable=False)

    consignment = db.relationship(
        'Consignment',
        backref='income_invoice_item',
        cascade='all, delete-orphan'
    )


class Service(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Integer, nullable=False)


class SaleInvoice(db.Model):

    __tablename__ = 'sale_invoice'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)

    items = db.relationship(
        'SaleInvoiceItem',
        backref='sale_invoice',
        lazy=True,
        cascade='all, delete-orphan'
    )

    @hybrid_property
    def total_price(self) -> int:
        return sum(map(lambda item: item.total_price, self.items))


class SaleInvoiceItem(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id', ondelete='CASCADE'), nullable=False)
    sale_id = db.Column(db.Integer, db.ForeignKey('sale_invoice.id', ondelete='CASCADE'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Integer, nullable=False)


class Consignment(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    consignment_number = db.Column(db.Integer, nullable=False)
    arrival_date = db.Column(db.DateTime, nullable=False)
    product_id = db.Column(
        db.Integer,
        db.ForeignKey('product.id', ondelete='CASCADE'),
        nullable=False
    )
    income_invoice_item_id = db.Column(
        db.Integer,
        db.ForeignKey('income_invoice_item.id', ondelete='CASCADE'),
        nullable=False
    )
    quantity = db.Column(db.Integer, nullable=False)
    current_quantity = db.Column(db.Integer, nullable=False)
    depreciated = db.Column(db.Boolean, default=False)
    total_price = db.Column(db.Integer, nullable=False)


@event.listens_for(IncomeInvoiceItem, 'after_delete')
def delete_empty_income_invoice(mapper, connection, target):
    invoice = target.income_invoice

    if not invoice.items:
        db.session.delete(invoice)


@event.listens_for(SaleInvoiceItem, 'after_delete')
def delete_empty_sale_invoice(mapper, connection, target):
    invoice = target.sale_invoice

    if not invoice.items:
        db.session.delete(invoice)


def init_db() -> None:
    """
    Puts some initialization data to database
    :return:
    """
    db.drop_all()
    db.create_all()
    db.session.commit()
    db.session.add(Product(name='Wheel', cost_price=5000))
    db.session.add(Product(name='Engine', cost_price=10000))
    db.session.commit()
