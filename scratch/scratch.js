const starWars = 'https://swapi.dev/api/films'



const firstLetter = "www.themealdb.com/api/json/v1/1/search.php?f=a"
const allIngredients = "www.themealdb.com/api/json/v1/1/list.php?i=list"




const ingredients = []
async function getIngredients(){
    let res = await axios.get(`https://${allIngredients}`)
    const meals = res.data.meals
    meals.forEach((ingredient) => {
        ingredients.push(ingredient.strIngredient)
    })
}

getIngredients()

console.log(ingredients)