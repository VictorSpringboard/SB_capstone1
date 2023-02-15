const API_KEY = 9973533
const QUERY = document.getElementById('nameInputBox')
// const QUERY = 'chicken'
async function getMealNameData(){
        const someData = await axios.get(`https://www.themealdb.com/api/json/v2/${API_KEY}/search.php?`, {params: {s: QUERY.value}} )
        console.log(someData.data)
    }
    
    const searchButton = document.querySelector('form.searchForm').addEventListener('submit', function (e) {
        e.preventDefault()
        // console.log(QUERY)
        // console.log(QUERY.value)
        getMealNameData()
})
