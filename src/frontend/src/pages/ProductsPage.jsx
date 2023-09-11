import React from "react";
import {
    InfiniteList,
    Datagrid,
    TextField,
    Resource,
    Create,
    number,
    required,
    SimpleForm,
    TextInput,
    NumberInput,
    Edit,
    EditButton,
    CreateButton,
    TopToolbar,
    DeleteButton,
} from 'react-admin'


const formatCostPrice = (value) => {
    if (typeof value == 'string') {
        return Number(value.split(' ')[0]);
    }
    return value
};


const ProductForm = () => (
    <SimpleForm>
        <TextInput
            source={'name'}
            label={'Name'}
            validate={required()}
        />
        <NumberInput
            source={'cost_price'}
            label={'Cost Price'}
            format={formatCostPrice}
            validate={[required(), number()]}
        />
    </SimpleForm>
)


const ProductActions = () => (
    <TopToolbar>
        <CreateButton/>
    </TopToolbar>
)


const ProductsList = () => (
    <InfiniteList pagination={false} actions={<ProductActions/>}>
        <Datagrid>
            <TextField source={'id'} sortable={false}/>
            <TextField source={'name'} sortable={false}/>
            <TextField source={'quantity'} sortable={false}/>
            <TextField source={'cost_price'} sortable={false}/>
            <EditButton/>
            <DeleteButton/>
        </Datagrid>
    </InfiniteList>
)

const ProductCreate = () => (
    <Create><ProductForm/></Create>
)

const ProductEdit = () => (
    <Edit><ProductForm/></Edit>
)


export default function ProductsPage () {
    return (
        <Resource
            name={'products'}
            list={<ProductsList/>}
            edit={<ProductEdit/>}
            create={<ProductCreate/>}
        />
    )
}
