import React from "react";
import {
    Admin,
    Menu,
    Layout,
    CustomRoutes
} from "react-admin";
import dataProvider from "./dataProvider";
import {Route} from 'react-router-dom';

import ShopTwoIcon from '@mui/icons-material/ShopTwo';
import ListAltIcon from '@mui/icons-material/ListAlt';
import RemoveCircleOutlineIcon from '@mui/icons-material/RemoveCircleOutline';
import AddCircleOutlineIcon from '@mui/icons-material/AddCircleOutline';
import DnsIcon from '@mui/icons-material/Dns';
import SummarizeIcon from '@mui/icons-material/Summarize';

import SubMenu from "./components/SubMenu";
import ProductsPage from "./pages/ProductsPage";
import ConsignmentsPage from "./pages/ConsignmentsPage";
import SaleInvoicesPage from "./pages/SaleInvoicesPage";
import IncomeInvoicesPage from "./pages/IncomeInvoicesPage";
import ReportsPage from "./pages/ReportsPage";


const DataMenu = () => (
    <Menu>
        <Menu.Item to={'products'} primaryText={'Products'} leftIcon={<ShopTwoIcon/>} />
        <Menu.Item to={'consignments'} primaryText={'Consignments'} leftIcon={<ListAltIcon/>} />
        <SubMenu primaryText={'Invoices'} leftIcon={<DnsIcon/>}>
            <Menu.Item to={'sale_invoices'} primaryText={'Sale Invoices'} leftIcon={<RemoveCircleOutlineIcon/>} />
            <Menu.Item to={'income_invoices'} primaryText={'Income Invoices'} leftIcon={<AddCircleOutlineIcon/>} />
        </SubMenu>
        <Menu.Item to={'reports'} primaryText={"Reports"} leftIcon={<SummarizeIcon/>} />
    </Menu>
)


const DataLayout = props => <Layout {...props} menu={DataMenu}/>


function App() {
    return (
        <Admin layout={DataLayout} dataProvider={dataProvider}>
            <CustomRoutes>
                <Route path={'products/*'} element={<ProductsPage/>}/>
                <Route path={'consignments/*'} element={<ConsignmentsPage/>}/>
                <Route path={'sale_invoices/*'} element={<SaleInvoicesPage/>}/>
                <Route path={'income_invoices/*'} element={<IncomeInvoicesPage/>}/>
                <Route path={'reports'} element={<ReportsPage/>}/>
            </CustomRoutes>
        </Admin>
    );
}

export default App;
