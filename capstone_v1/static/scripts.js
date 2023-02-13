const API_KEY = 9973533
const QUERY = 'chicken'

async function getSomeData(){
        const someData = await axios.get(`https://www.themealdb.com/api/json/v2/${API_KEY}/search.php?s=${QUERY}`)
        console.log(someData.data)
    }
getSomeData()
