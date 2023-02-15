const API_KEY = 9973533
const QUERY = document.getElementById('searchBox')

const theList = document.querySelector('.stuff')

const mealIdList = []
async function getSomeData(){
        const someData = await axios.get(`https://www.themealdb.com/api/json/v2/${API_KEY}/filter.php?`, {params:{i:QUERY.value}})
        console.log(someData.data)

        for (let meal of someData.data.meals){
            mealIdList.push(meal.idMeal)
        }
        console.log('The Meal id List is')
        console.log(mealIdList.length)
        console.log(mealIdList)


        // This is where the cards for each meal get made (I'll use bootstrap cards for each meal)


        // bootstrap card etc etc etc
        
}


const searchButton = document.querySelector('#searchForm').addEventListener('submit', (e)=>{
    e.preventDefault()
    getSomeData()
})
 
async function getMealData(id){
    const someData = await axios.get(`https://www.themealdb.com/api/json/v2/${API_KEY}/lookup.php?`, {params:{i:id}})
        console.log(someData.data)
}

getMealData(52772)
