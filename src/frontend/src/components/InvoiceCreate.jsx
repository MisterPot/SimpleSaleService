import React from "react";
import {
    Create,
    SimpleForm,
    NumberInput,
    DateTimeInput,
    SimpleFormIterator,
    ArrayInput,
    useGetList,
    Loading,
    SelectInput,
    FormDataConsumer,
    maxValue,
    number,
    required
} from 'react-admin'


export default function IncomeCreate (props) {

    const {data, isLoading, error} = useGetList(
        'products',
        {
        pagination: {page: 1, perPage: 10},
        sort: {field: 'id', order:'DESC'}
    })
    const {doCheck} = props

    if (isLoading) return <Loading/>
    if (error) return <p>ERROR</p>

    return (
        <Create>
            <SimpleForm>
                <DateTimeInput required label={'Creation date'} source={'date'}/>
                <ArrayInput source={'items'} validate={required()}>
                    <SimpleFormIterator inline>
                        <SelectInput
                            required
                            label={'Product'}
                            choices={data}
                            source={'product_id'}
                        />
                        <FormDataConsumer>
                            {({scopedFormData, getSource}) => {
                                const currentSupply = scopedFormData.product_id !== null
                                    ? data.find(value => value.id === scopedFormData.product_id)?.quantity
                                    : '0'
                                return (
                                    <NumberInput
                                        required
                                        label={`Quantity (${currentSupply} items)`}
                                        source={getSource('quantity')}
                                        validate={[
                                            number(),
                                            doCheck ? maxValue(currentSupply, 'Invalid quantity') : () => {}
                                        ]}
                                    />
                                )
                            }}
                        </FormDataConsumer>
                        <NumberInput required label={'Total price'} source={'total_price'}/>
                        {props.children}
                    </SimpleFormIterator>
                </ArrayInput>
            </SimpleForm>
        </Create>
    )
}
