// This code handles the re-ordering of the favorites list
var p = document.getElementsByTagName('p')
var choice = document.getElementsByClassName('choice')
var dragItem = null;

for (var i of p){
    i.addEventListener('dragstart', dragStart)
    i.addEventListener('dragend', dragEnd)
}

function dragStart(){
    dragItem = this
    setTimeout(() => this.style.display = 'none', 0)
}


function dragEnd(){
    setTimeout(() => this.style.display = 'block', 0 )
    dragItem = null;
}

for (var j of choice){
    j.addEventListener('dragover', dragOver)
    j.addEventListener('dragenter', dragEnter)
    j.addEventListener('dragLeave', dragLeave)
    j.addEventListener('drop', drop)
}

function drop(){
    this.append(dragItem)
}

function dragOver(e){
    e.preventDefault()
    this.style.border = '2px dotted cyan'
}

function dragEnter(e){
    e.preventDefault() 

}

function dragLeave(e){
    this.style.border = 'none'
}

    
const API_KEY = 9973533
const QUERY = document.getElementById('searchBox')

// const $theList = document.querySelector('.stuff')
const $theList = $('.stuff')


const mealIds = []
const mealPromises = []
const mealObjs = []
async function getSomeData(){
        const someData = await axios.get(`https://www.themealdb.com/api/json/v2/${API_KEY}/filter.php?`, {params:{i:QUERY.value}})
        .then(res => {
            // console.log(res.data.meals)
            for (let mealId of res.data.meals){
                mealIds.push(parseInt(mealId.idMeal, 10))
            }    
        }).then(() => {
            
            for (let id of mealIds){
                const moreData = axios.get(`https://www.themealdb.com/api/json/v2/${API_KEY}/lookup.php?`, {params: {i:id}})
                mealPromises.push(moreData)
            }    
        })    
            Promise.all(mealPromises)
            .then(arr =>{
                // console.log(arr[0].data.meals[0].strMeal)
                for (let i = 0; i < mealPromises.length; i++){
                    mealObjs.push(arr[i].data.meals[0])
                }    
            }).then(()=>{  
                for (let mealItem of mealObjs){
                    const item = document.createElement('div')
                    $theList.append(item)
                    $theList.append(`<div class="card" style="width: 18rem;">
                                    <img class="card-img-top" src=".../100px180/" alt="Card image cap">
                                        <div class="card-body">
                                            <h5 class="card-title">${mealItem.strMeal}</h5>
                                            <p class="card-text">${mealItem.strInstructions}</p>
                                            <a href="/recipe_details/${mealItem.idMeal}" class="btn btn-primary">Go somewhere</a>
                                        </div>    
                                </div>`)        
                }                

            })    
                
}            







const searchButton = document.querySelector('#searchForm').addEventListener('submit', (e)=>{
    e.preventDefault()
    getSomeData()

})    


