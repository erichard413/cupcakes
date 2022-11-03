const BASE_URL = "http://127.0.0.1:5000/api";
const cupsection = document.querySelector('#cupcakeslist');

window.onload = getCupcakes();

cupcakeList = document.getElementById("cupcakeslist")

function generateMarkup(cupcake) {
  return `<p class="title">${capitalize(cupcake.flavor)}</p><div class="photo"><img src="${cupcake.image}" alt="cupcake"></div><div class="details"> <p>Size: ${capitalize(cupcake.size)}</p> <p>Rating: ${cupcake.rating}</p></div> <button class="deletebtn" id="${cupcake.id}">Delete</button>`
}

function capitalize(str){
  return str.charAt(0).toUpperCase() + str.slice(1);
}

function formatRes(cup){
  const newDiv = document.createElement('div');
  newDiv.classList.add(`cupcake_div`)
  newDiv.id = cup.id
  newDiv.innerHTML = generateMarkup(cup)
  cupsection.append(newDiv)
}

async function getCupcakes() {
  const res = await axios.get(`${BASE_URL}/cupcakes`);
  
    for (let cup of res.data.cupcakes) {
      formatRes(cup)
      // const newDiv = document.createElement('div');
      // newDiv.classList.add('cupcake_div')
      // newDiv.innerHTML = generateMarkup(cup)
      // cupsection.append(newDiv)
    }
  }

addBtn = document.getElementById("addbtn")
addBtn.addEventListener('click', async function(e){
  e.preventDefault()
  const flavor = document.getElementById('form-flavor').value
  const size = document.getElementById('form-size').value
  const rating = document.getElementById('form-rating').value
  const image = document.getElementById('form-image').value
  const cup = {'flavor':flavor,'size':size,'rating':rating,'image':image}
  const newCupcakeRes = await axios.post(`${BASE_URL}/cupcakes`, cup)
  const newCup = newCupcakeRes.data.cupcake
  formatRes(newCup)
})

deleteBtn = document.getElementById("cupcakeslist")
deleteBtn.addEventListener('click', async function(e){
  e.preventDefault()
  if (e.target.classList.value === "deletebtn") {
    cupId = e.target.id
    deleted = await axios.delete(`${BASE_URL}/cupcakes/${cupId}`)
    cupcake = document.getElementById(cupId)
    cupcakeList.removeChild(cupcake)
  }
  })

// async function newCupcake(cup) {
//   await axios.post(`${BASE_URL}/cupcakes`, cup)
// }

// flavor = request.json["flavor"]
//     size = request.json["size"]
//     rating = request.json["rating"]
//     image = request.json["image"]