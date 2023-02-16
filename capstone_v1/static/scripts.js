const API_KEY = 9973533
const QUERY = document.getElementById('searchBox')

// const $theList = document.querySelector('.stuff')
const $theList = $('.stuff')


const mealIdList = []
const mealList = []
const fullMeals = []
async function getSomeData(){
        const someData = await axios.get(`https://www.themealdb.com/api/json/v2/${API_KEY}/filter.php?`, {params:{i:QUERY.value}})
        .then(res => {
            // console.log(res.data.meals)
            for (let mealId of res.data.meals){
                mealIdList.push(parseInt(mealId.idMeal, 10))
            }
        }).then(() => {
            
            for (let id of mealIdList){
                const moreData = axios.get(`https://www.themealdb.com/api/json/v2/${API_KEY}/lookup.php?`, {params: {i:id}})
                mealList.push(moreData)
            }
        })
            Promise.all(mealList)
            .then(arr =>{
                // console.log(arr[0].data.meals[0].strMeal)
                for (let i = 0; i < mealList.length; i++){
                    fullMeals.push(arr[i].data.meals[0])
                }
            }).then(()=>{
                console.log(fullMeals)
                console.log('first fart')
                for (let j = 0; j < fullMeals.length; j++){
                    console.log(j)
                }
                for (let mealItem of fullMeals){
                    console.log(mealItem.strMeal)
                    const item = document.createElement('div')
                    $theList.append(item)
                    $theList.append(`<div class="card" style="width: 18rem;">
                                    <img class="card-img-top" src=".../100px180/" alt="Card image cap">
                                        <div class="card-body">
                                            <h5 class="card-title">${mealItem.strMeal}</h5>
                                            <p class="card-text">${mealItem.strInstructions}</p>
                                            <a href="#" class="btn btn-primary">Go somewhere</a>
                                        </div>
                                </div>`)
                }

            })
                // const item = document.createElement('div')
                // $theList.append(item)
                // $theList.append(`<div class="card" style="width: 18rem;">
                //                     <img class="card-img-top" src=".../100px180/" alt="Card image cap">
                //                         <div class="card-body">
                //                             <h5 class="card-title">${meal[0]}</h5>
                //                             <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
                //                             <a href="#" class="btn btn-primary">Go somewhere</a>
                //                         </div>
                //                 </div>`)
    
}





// This is where the cards for each meal get made (I'll use bootstrap cards for each meal)



const searchButton = document.querySelector('#searchForm').addEventListener('submit', (e)=>{
    e.preventDefault()
    console.log('a')
    getSomeData()
    console.log('b')
})
