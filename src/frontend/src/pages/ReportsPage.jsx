import React, {useState} from "react";
import {
    useNotify,
} from "react-admin";
import {DateTimePicker} from '@mui/x-date-pickers/DateTimePicker';
import {LocalizationProvider} from '@mui/x-date-pickers/LocalizationProvider';
import {AdapterDayjs} from '@mui/x-date-pickers/AdapterDayjs';
import {
    Paper,
    Select,
    MenuItem,
    FormControl,
    Button
} from "@mui/material";
import {apiUrl} from "../dataProvider";
import dayjs from "dayjs";


const ReportForm = () => {
    const [loading, setLoading] = useState(false)
    const [reportType, setReportType] = useState('product')
    const [data, setData] = useState({})
    const notify = useNotify()

    const onSubmit = (e) => {
        e.preventDefault()
        setLoading(true)

        const isInvoiceReport = data.report_type === 'income' || data.report_type === 'sale'

        if (isInvoiceReport && !(dayjs(data?.start_time).unix() <= dayjs(data?.end_time).unix())) {
            notify("Start time can't be greater then end time", {type: 'error'})
            setLoading(false)
            return
        }

        fetch(apiUrl + '/report',
            {
                method: 'POST',
                body: JSON.stringify(data),
                headers: {
                    'Content-Type': 'application/json'
                }
            }
        ).then(
            res => res.json()
        ).then(
            data => window.open(apiUrl + data.url, '_blank').focus()
        ).catch(e => {
            notify(`Error: cant't create report. Fields missing`, {type: 'error'})
        }).finally(() => {
            setLoading(false)
        })
    }

    const toField = (fieldName) => (event) => {
        setData((prevState => {
            return {
                ...prevState,
                [fieldName]: event.toISOString()
            }
        }))
    }

    return (
        <FormControl fullWidth>
            <LocalizationProvider dateAdapter={AdapterDayjs}>
                <Select
                    disabled={loading}
                    value={reportType}
                    onChange={e => {
                        setReportType(e.target.value)
                        setData({report_type: e.target.value})
                    }}
                    required
                >
                    <MenuItem value={'sale'}>Sale</MenuItem>
                    <MenuItem value={'income'}>Income</MenuItem>
                    <MenuItem value={'product'}>Product</MenuItem>
                </Select>
                {
                    (reportType === 'sale' || reportType === 'income') &&
                    <>
                        <DateTimePicker
                            label={'Start time'}
                            disabled={loading}
                            onChange={toField('start_time')}
                        />
                        <DateTimePicker
                            label={'End time'}
                            disabled={loading}
                            onChange={toField('end_time')}
                        />
                    </>
                }
                {
                    (reportType === 'product') &&
                    <DateTimePicker
                        label={'Date'}
                        source={'date'}
                        disabled={loading}
                        onChange={toField('date')}

                        slotProps={{
                            textField:{
                                required: true
                            }
                        }}
                    />
                }
                <Button type={'submit'} onClick={onSubmit}>Submit</Button>
            </LocalizationProvider>
        </FormControl>
    )
}

export default function ReportsPage () {
    return (
        <Paper style={{width: '50%', margin: '0 auto'}}>
            <ReportForm/>
        </Paper>
    )
}
