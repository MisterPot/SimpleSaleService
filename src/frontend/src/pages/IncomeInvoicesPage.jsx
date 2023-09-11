import React from "react";
import {Resource, DateTimeInput,} from 'react-admin'
import InvoiceList from "../components/InvoiceList";
import InvoiceCreate from "../components/InvoiceCreate";


const IncomeCreate = () => (
    <InvoiceCreate>
        <DateTimeInput label={'Arrival date'} required source={'arrival_date'} />
    </InvoiceCreate>
)


export default function IncomeInvoicePage () {
    return (
        <Resource name={'income_invoices'} list={<InvoiceList/>} create={<IncomeCreate/>}/>
    )
}