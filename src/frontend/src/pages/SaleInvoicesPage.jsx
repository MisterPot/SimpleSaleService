import React from "react";
import {Resource} from 'react-admin'
import InvoiceList from "../components/InvoiceList";
import InvoiceCreate from "../components/InvoiceCreate";


export default function SaleInvoicesPage () {
    return (
        <Resource name={'sale_invoices'} list={<InvoiceList/>} create={<InvoiceCreate doCheck={true}/>}/>
    )
}
