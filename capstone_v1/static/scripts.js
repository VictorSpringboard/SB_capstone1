const API_KEY = 9973533
const QUERY = document.getElementById('searchBox')

// const $theList = document.querySelector('.stuff')
const $theList = $('.stuff')


const mealIdList = []
async function getSomeData(){
        const someData = await axios.get(`https://www.themealdb.com/api/json/v2/${API_KEY}/filter.php?`, {params:{i:QUERY.value}})
        // console.log(someData.data)

        for (let meal of someData.data.meals){
            mealIdList.push(parseInt(meal.idMeal, 10))
        }
        // console.log(mealIdList)


        const getMeal = () => {
        for (let meal of mealIdList.slice(0,5)){
            async function getMealInfo(){
                const mealData = await axios.get(`www.themealdb.com/api/json/v1/${API_KEY}/lookup.php?`, {params: {i:meal}})
                console.log(mealData)
            }
            getMealInfo()
            }
            getMeal()
        }
    }





// This is where the cards for each meal get made (I'll use bootstrap cards for each meal)
//         const item = document.createElement('div')
//         $theList.append(item)
//         $theList.append(`<div class="card" style="width: 18rem;">
//             <img class="card-img-top" src=".../100px180/" alt="Card image cap">
//                 <div class="card-body">
//                     <h5 class="card-title">Hello?</h5>
//                     <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
//                     <a href="#" class="btn btn-primary">Go somewhere</a>
//                 </div>
//             </div>`)
// }



const searchButton = document.querySelector('#searchForm').addEventListener('submit', (e)=>{
    e.preventDefault()
    console.log('a')
    getSomeData()
    console.log('b')
    // getMeal()
    console.log('c')
})
