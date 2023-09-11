import React from "react";
import {
    InfiniteList,
    Datagrid,
    TextField,
    Resource,
    useGetList,
    Loading,
    FunctionField
} from 'react-admin'


const ConsignmentsList = () => {

    const {data, isLoading, error} = useGetList(
        'products',
        {
            pagination: {page: 1, perPage: 10},
            sort: {field: 'id', order:'DESC'}
        })

    if (isLoading) return <Loading/>
    if (error) return <p>ERROR</p>

    return (
        <InfiniteList pagination={false}>
            <Datagrid>
                <TextField source={'id'} sortable={false}/>
                <TextField source={'consignment_number'} sortable={false}/>
                <TextField source={'arrival_date'} sortable={false}/>
                <FunctionField
                    label={'Product Name'}
                    render={record => data.find(value => value.id === record.product_id)?.name}
                />
                <TextField source={'quantity'} sortable={false}/>
                <TextField source={'current_quantity'} sortable={false}/>
                <TextField source={'depreciated'} sortable={false}/>
                <TextField source={'total_price'} sortable={false}/>
            </Datagrid>
        </InfiniteList>
    )
}



export default function ConsignmentsPage () {
    return (
        <Resource name={'consignments'} list={<ConsignmentsList/>}/>
    )
}
