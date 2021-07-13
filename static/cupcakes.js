function createCupcakeHTML(cupcake) {
    return `<div>
      <li data-id="${cupcake.id}">
        <img class="image img-thumbnail" src="${cupcake.image}">
        Flavor: ${cupcake.flavor}, Size: ${cupcake.size}, Rating: ${cupcake.rating}
        <button class="delete-cupcake btn-sm btn-danger">DELETE</button>
      </li>
    </div>`;
  }
  
async function showCupcakeList() {
  const response = await axios.get(`http://127.0.0.1:5000/api/cupcakes`);    
  for (let cupcakeInfo of response.data.cupcakes) {
    let cupcake = $(createCupcakeHTML(cupcakeInfo));
    $("#cupcake-list").append(cupcake);
  }
}

$("#new-cupcake-form").on("submit", async function(e) {
    e.preventDefault();
    
    let flavor= $("#flavor").val();
    let size= $("#size").val();
    let rating= $("#rating").val();
    let image= $("#image").val();
    const cupcakeResponse = await axios.post(`http://127.0.0.1:5000/api/cupcakes`, {flavor, size, rating, image});
    let cupcake = $(createCupcakeHTML(cupcakeResponse.data.cupcake));
    $("#cupcake-list").append(cupcake);
});
  
$('#cupcake-list').on("click", '.delete-cupcake', async function (e) {
  e.preventDefault();
  let $cupcake = $(e.target).closest('li');
  let id = $cupcake.attr('data-id');
  await axios.delete(`http://127.0.0.1:5000/api/cupcakes/${id}`);
  $cupcake.remove();
});

showCupcakeList();
