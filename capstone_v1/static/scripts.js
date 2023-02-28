const draggable_list = document.getElementById('draggable-list');
const check = document.getElementById('check');

const richestPeople = [
  'Jeff Bezos',
  'Bill Gates',
  'Warren Buffett',
  'Bernard Arnault',
  'Carlos Slim Helu',
  'Amancio Ortega',
  'Larry Ellison',
  'Mark Zuckerberg',
  'Michael Bloomberg',
  'Larry Page'
];

// Store listitems
const listItems = [];

let dragStartIndex;

createList();

// Insert list items into DOM
function createList() {
  [...richestPeople]
    .map(a => ({ value: a, sort: Math.random() }))
    .sort((a, b) => a.sort - b.sort)
    .map(a => a.value)
    .forEach((person, index) => {
      const listItem = document.createElement('li');

      listItem.setAttribute('data-index', index);

      listItem.innerHTML = `
        <span class="number">${index + 1}</span>
        <div class="draggable" draggable="true">
          <p class="person-name">${person}</p>
          <i class="fas fa-grip-lines"></i>
        </div>
      `;

      listItems.push(listItem);

      draggable_list.appendChild(listItem);
    });

  addEventListeners();
}

function dragStart() {
  // console.log('Event: ', 'dragstart');
  dragStartIndex = +this.closest('li').getAttribute('data-index');
}

function dragEnter() {
  // console.log('Event: ', 'dragenter');
  this.classList.add('over');
}

function dragLeave() {
  // console.log('Event: ', 'dragleave');
  this.classList.remove('over');
}

function dragOver(e) {
  // console.log('Event: ', 'dragover');
  e.preventDefault();
}

function dragDrop() {
  // console.log('Event: ', 'drop');
  const dragEndIndex = +this.getAttribute('data-index');
  swapItems(dragStartIndex, dragEndIndex);

  this.classList.remove('over');
}

// Swap list items that are drag and drop
function swapItems(fromIndex, toIndex) {
  const itemOne = listItems[fromIndex].querySelector('.draggable');
  const itemTwo = listItems[toIndex].querySelector('.draggable');

  listItems[fromIndex].appendChild(itemTwo);
  listItems[toIndex].appendChild(itemOne);
}

// Check the order of list items
function checkOrder() {
  listItems.forEach((listItem, index) => {
    const personName = listItem.querySelector('.draggable').innerText.trim();

    if (personName !== richestPeople[index]) {
      listItem.classList.add('wrong');
    } else {
      listItem.classList.remove('wrong');
      listItem.classList.add('right');
    }
  });
}

function addEventListeners() {
  const draggables = document.querySelectorAll('.draggable');
  const dragListItems = document.querySelectorAll('.draggable-list li');

  draggables.forEach(draggable => {
    draggable.addEventListener('dragstart', dragStart);
  });

  dragListItems.forEach(item => {
    item.addEventListener('dragover', dragOver);
    item.addEventListener('drop', dragDrop);
    item.addEventListener('dragenter', dragEnter);
    item.addEventListener('dragleave', dragLeave);
  });
}

check.addEventListener('click', checkOrder);

    
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


