import Provider from "ra-data-json-server";

export const apiUrl = 'http://localhost:7767'
const dataProvider = Provider(apiUrl)
export default dataProvider
