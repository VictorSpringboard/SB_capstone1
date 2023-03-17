const fav_holders = document.querySelectorAll('.fav-holder')
const top_3 = document.querySelectorAll('.top-3')


const toggleClasses = (e, classes) =>{
    classes.forEach((className) => {
        e.classList.toggle(className)
    })
}
const classes = [
    'fav-holder',
    'top-3'
]

fav_holders.forEach((fav) => {
    fav.addEventListener('click', () => {
        toggleClasses(fav, classes)
    })
})

top_3.forEach((fav) => {
    fav.addEventListener('click', () => {
        toggleClasses(fav, classes)
    })
})