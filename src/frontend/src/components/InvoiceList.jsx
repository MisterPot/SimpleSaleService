import {
    Datagrid,
    InfiniteList,
    TextField,
    TopToolbar,
    CreateButton,
    useResourceContext,
    SimpleShowLayout,
    ArrayField,
    useGetList,
    Loading,
    FunctionField,
    useRecordContext,
    NumberField,
    DeleteButton,
} from "react-admin";
import {
    Typography,
    Box,
} from '@mui/material'
import React from "react";


const Empty = () => {
    const resource = useResourceContext()

    return (
        <Box textAlign="center" style={{margin: '0 auto', top: '50%', position: 'relative'}}>
            <Typography variant="h4" paragraph>
                {`No ${resource} available`}
            </Typography>
            <Typography variant="body1">
                Create one invoice
            </Typography>
            <CreateButton />
        </Box>
    )
}


const TopActions = () => (
    <TopToolbar>
        <CreateButton/>
    </TopToolbar>
)


const RowExpand = ({products}) => {

    const record = useRecordContext()
    const getProductName = record => {
        return `${products.find(product => product.id === record.product_id)?.name}`
    }

    return (
        <SimpleShowLayout>
            <ArrayField source={'items'} label={'Invoice items'}>
                <Datagrid bulkActionButtons={false} optimized size={'small'}>
                    <FunctionField label={'Product Name'} render={getProductName} />
                    {
                        record.items[0].arrival_date && <TextField source={'arrival_date'} label={'Arrival date'} sortable={false}/>
                    }
                    <NumberField source={'quantity'} label={'Quantity'} sortable={false}/>
                    <TextField source={'total_price'} label={'Total Price'} sortable={false}/>
                </Datagrid>
            </ArrayField>
        </SimpleShowLayout>
    )
}


export default function InvoiceList (props) {
    const {data, isLoading, error} = useGetList(
    'products',
    {
        pagination: {page: 1, perPage: 10},
        sort: {field: 'id', order:'DESC'}
    })

    if (isLoading) return <Loading/>
    if (error) return <p>ERROR</p>

    return (
        <InfiniteList pagination={false} actions={<TopActions/>} empty={<Empty/>}>
            <Datagrid expand={<RowExpand products={data}/>}>
                <TextField source={'id'} sortable={false}/>
                <TextField source={'date'} sortable={false}/>
                <TextField source={'total_price'} sortable={false}/>
                <DeleteButton/>
                {props.children}
            </Datagrid>
        </InfiniteList>
    )
}
