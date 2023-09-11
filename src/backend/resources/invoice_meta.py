from typing import (
    Tuple,
    Union,
    Callable
)

from flask import (
    Response,
    make_response,
    request
)
from flask_restful import (
    Resource,
    fields,
    marshal_with,
    marshal_with_field
)

from ..controller import BusinessController, InvoiceType
from ..models import db
from ..utils import with_count


class InvoiceMeta:
    __model__ = None
    __invoice_type__ = None


class ListInvoiceResourceMeta(Resource, InvoiceMeta):
    """
    Represents a list of model.
    Can add new items to model
    """

    def options(self) -> Response:
        return make_response()

    def get(self):
        return self.__model__.query.all()

    def post(self) -> str:
        BusinessController.create_invoice(
            invoice_type=self.__invoice_type__,
            creation_date=BusinessController.parse_time(request.json['date']),
            invoice_items=list(map(BusinessController.create_item_from_json, request.json['items']))
        )
        return 'OK'


class SingleInvoiceResourceMeta(Resource, InvoiceMeta):
    """
    Represents a resource, which will send only 1 item by id
    and manages model changes
    """

    def get(self, invoice_id: int):
        return self.__model__.query.get(invoice_id)

    def options(self) -> Response:
        return make_response()

    def delete(self, invoice_id: int) -> int:
        product = self.__model__.query.get(invoice_id)
        db.session.delete(product)
        db.session.commit()
        return invoice_id


def use_marshal(
        field: Union[fields.Raw, dict],
        function: Callable,
        with_field: bool = False
) -> Callable:
    """
    Help function to wrap route with fields
    :param field: to wrap
    :param function: route to wrap
    :param with_field: use `marshal_with_field` or `marshal_with`
    :return:
    """
    if with_field:
        return marshal_with_field(field)(function)
    return marshal_with(field)(function)


def create_invoice_resource(
        invoice_model,
        invoice_type: InvoiceType,
        model_fields: dict,
        name: str,
) -> Tuple[ListInvoiceResourceMeta, SingleInvoiceResourceMeta]:
    """
    Function, which creates resource with described below template
    :param name: resource name
    :param invoice_model: model, which will be used for resources
    :param invoice_type: model invoice type
    :param model_fields: fields, which uses for marshaling
    :return:
    """
    vars_dict = {
        "__invoice_type__": invoice_type,
        "__model__": invoice_model,
    }

    list_resource = type(
        f'List{name}',
        (ListInvoiceResourceMeta,),
        vars_dict,
    )
    single_resource = type(
        f'Single{name}',
        (SingleInvoiceResourceMeta,),
        vars_dict,
    )

    list_resource.get = with_count(invoice_model)(
        use_marshal(
            field=fields.List(fields.Nested(model_fields)),
            function=list_resource.get,
            with_field=True
        )
    )
    list_resource.post = use_marshal(field=model_fields, function=list_resource.post)

    single_resource.get = use_marshal(field=model_fields, function=single_resource.get)

    return list_resource, single_resource
