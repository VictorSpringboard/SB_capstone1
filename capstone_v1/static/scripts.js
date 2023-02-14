const API_KEY = 9973533
const QUERY = document.getElementById('searchBox')

const theList = document.querySelector('.stuff')

async function getSomeData(){
        const someData = await axios.get(`https://www.themealdb.com/api/json/v2/${API_KEY}/search.php?`, {params:{s:QUERY.value}})
        // console.log(someData.data.meals)

        for (let meal of someData.data.meals){
            console.log(meal.strMeal)
            const item = document.createElement('li')
            item.innerHTML = meal.strMeal
            theList.appendChild(item)
        }
}

const searchButton = document.querySelector('#searchForm').addEventListener('submit', (e)=>{
    e.preventDefault()
    getSomeData()
})
